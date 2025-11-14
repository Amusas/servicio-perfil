# Servicio de Perfil de Usuario

Microservicio desarrollado en Python con FastAPI para gestionar perfiles de usuario. Este servicio permite a los usuarios autenticados actualizar su información de perfil personal.

## 🚀 Características

- ✅ **API REST** para gestión de perfiles
- ✅ **Validación de tokens JWT** generados por el servicio de usuarios
- ✅ **Autenticación y autorización** - Los usuarios solo pueden acceder a su propio perfil
- ✅ **Logs en formato JSON** con estructura consistente
- ✅ **Conexión a PostgreSQL** con pool de conexiones
- ✅ **Manejo robusto de errores**

## 📋 Campos del Perfil

El perfil de usuario incluye los siguientes campos:

- **personal_url**: URL de página personal
- **nickname**: Apodo del usuario
- **is_contact_public**: Si la información de contacto es pública o no
- **mailing_address**: Dirección de correspondencia
- **biography**: Biografía del usuario
- **organization**: Organización a la que pertenece
- **country**: País de residencia
- **social_links**: Links de redes sociales (JSON)

## 🛠️ Instalación

```bash
cd servicio-perfil
pip install -r requirements.txt
```

## 🔧 Configuración

Las variables de entorno se configuran en el `docker-compose.yml`:

```env
DB_HOST=database
DB_PORT=5432
DB_USER=admin_user
DB_PASSWORD=supersecurepassword
DB_NAME=usuariosdb
PUBLIC_KEY_PATH=/app/keys/public-key.pem
PORT=8087
```

## 🚀 Ejecución

### Desarrollo local

```bash
python main.py
```

El servicio estará disponible en `http://localhost:8087`

### Docker

```bash
docker-compose up servicio-perfil
```

## 📡 Endpoints Disponibles

### 1. **GET /api/v1/profiles/{user_id}** - Obtener Perfil

Obtiene el perfil de un usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "personal_url": "https://example.com",
  "nickname": "johndoe",
  "is_contact_public": true,
  "mailing_address": "123 Main St",
  "biography": "Software developer",
  "organization": "Tech Corp",
  "country": "Colombia",
  "social_links": {
    "twitter": "https://twitter.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 2. **PUT /api/v1/profiles/{user_id}** - Actualizar Perfil

Actualiza el perfil de un usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body (todos los campos son opcionales):**
```json
{
  "personal_url": "https://example.com",
  "nickname": "johndoe",
  "is_contact_public": true,
  "mailing_address": "123 Main St",
  "biography": "Software developer",
  "organization": "Tech Corp",
  "country": "Colombia",
  "social_links": {
    "twitter": "https://twitter.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe"
  }
}
```

**Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "personal_url": "https://example.com",
  "nickname": "johndoe",
  "is_contact_public": true,
  "mailing_address": "123 Main St",
  "biography": "Software developer",
  "organization": "Tech Corp",
  "country": "Colombia",
  "social_links": {
    "twitter": "https://twitter.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### 3. **GET /health** - Health Check

Verifica el estado del servicio.

**Respuesta (200):**
```json
{
  "status": "healthy",
  "service": "profile-service"
}
```

## 🔐 Seguridad

- **Validación de tokens JWT**: Todos los endpoints requieren un token JWT válido
- **Autorización**: Los usuarios solo pueden acceder y modificar su propio perfil
- **Validación de issuer**: Se verifica que el token sea emitido por "ingesis.uniquindio.edu.co"
- **Verificación de expiración**: Los tokens expirados son rechazados automáticamente

## 📊 Base de Datos

La tabla `profiles` tiene la siguiente estructura:

```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    personal_url VARCHAR(500),
    nickname VARCHAR(100),
    is_contact_public BOOLEAN NOT NULL DEFAULT false,
    mailing_address TEXT,
    biography TEXT,
    organization VARCHAR(200),
    country VARCHAR(100),
    social_links JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_profile_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 📝 Logs

Los logs se generan en formato JSON con la siguiente estructura:

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "logger": "[ProfileController]",
  "message": "Obteniendo perfil",
  "thread": "12345",
  "userId": 1
}
```

## 🏗️ Estructura del Proyecto

```
servicio-perfil/
├── config/
│   ├── __init__.py
│   ├── database.py          # Configuración de base de datos
│   └── jwt_config.py        # Configuración de JWT
├── controllers/
│   ├── __init__.py
│   └── profile_controller.py # Lógica de negocio
├── logger/
│   ├── __init__.py
│   └── logger.py            # Logger en formato JSON
├── middleware/
│   ├── __init__.py
│   └── jwt_middleware.py    # Validación de tokens JWT
├── models/
│   ├── __init__.py
│   └── profile.py           # Modelos Pydantic
├── repositories/
│   ├── __init__.py
│   └── profile_repository.py # Acceso a datos
├── routes/
│   ├── __init__.py
│   └── profile_routes.py    # Definición de rutas
├── Dockerfile
├── main.py                  # Punto de entrada
├── requirements.txt
└── README.md
```

## 🔄 Integración

Este servicio se integra con:

- **servicio-usuarios**: Valida tokens JWT generados por este servicio
- **servicio-datos**: Crea automáticamente un perfil cuando se crea un usuario
- **database**: Comparte la base de datos PostgreSQL con otros servicios

## 📦 Dependencias

- **FastAPI**: Framework web moderno y rápido
- **uvicorn**: Servidor ASGI
- **psycopg2-binary**: Driver de PostgreSQL
- **python-jose**: Validación de tokens JWT
- **pydantic**: Validación de datos
- **cryptography**: Manejo de claves RSA

# servicio-perfil
