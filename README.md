# Get Your Age! 🧮👥

## Descripción del Proyecto

Get Your Age es un proyecto de microservicios que demuestra una arquitectura moderna de servicios web utilizando Flask, con un enfoque en la sincronización de datos mediante un patrón simplificado de Event Sourcing.

## Características Principales

- 🚀 Arquitectura de Microservicios
- 🔐 Autenticación con JWT
- 📊 Gestión de usuarios y edades
- 🔄 Event Sourcing simplificado
- 🛡️ Mecanismos de tolerancia a fallos (Circuit Breaker y reintentos)

## Estructura del Proyecto

```
project-root/
│
├── user_app.py        # Servicio de Usuarios
├── age_app.py         # Servicio de Edades
├── models.py          # Modelos de datos compartidos
└── requirements.txt   # Dependencias del proyecto
```

### Servicios

1. **User Service** (`user_app.py`):
   - Creación de usuarios
   - Generación de tokens JWT
   - Gestión de información básica de usuarios

2. **Age Service** (`age_app.py`):
   - Consulta y almacenamiento de edades
   - Sincronización de eventos de usuarios

## Tecnologías Utilizadas

- **Backend:** Python
- **Framework:** Flask
- **Base de Datos:** SQLAlchemy
- **Autenticación:** JWT
- **Patrón de Comunicación:** Event Sourcing
- **Resiliencia:** Circuit Breaker, Tenacity

## Requisitos Previos

- Python 3.8+
- pip

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/get-your-age.git
   cd get-your-age
   ```

2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Unix/macOS
   # o
   venv\Scripts\activate  # En Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

### Variables de Entorno

Crea un archivo `.env` con las siguientes variables:
```
SECRET_KEY=tu_clave_secreta_jwt
DATABASE_URL=sqlite:///users.db
```

## Ejecución

1. Iniciar el User Service:
   ```bash
   python user_app.py
   ```

2. En otra terminal, iniciar el Age Service:
   ```bash
   python age_app.py
   ```

## Endpoints

### Crear Usuario

- **URL:** `/users`
- **Método:** POST
- **Payload:**
  ```json
  {
    "name": "John Doe",
    "age": 30,
    "username": "johndoe"
  }
  ```

### Consultar Edad de Usuario

- **URL:** `/user_age`
- **Método:** POST
- **Payload:**
  ```json
  {
    "user_id": "1"
  }
  ```

## Patrón de Event Sourcing

El proyecto implementa un Event Sourcing simplificado:
1. Creación de usuario genera un evento "UserCreated"
2. El evento se propaga al Age Service
3. Age Service almacena información de edad para consultas futuras

## Próximas Mejoras

- [ ] Implementar sistema de mensajería con RabbitMQ o Kafka
- [ ] Aumentar cobertura de pruebas unitarias e integración
- [ ] Mejorar manejo de errores
- [ ] Añadir logging estructurado
- [ ] Implementar contenedorización con Docker

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Abre un issue para discutir cambios propuestos
2. Realiza un fork del repositorio
3. Crea tu rama de características
4. Envía un pull request

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## Contacto

Para dudas o sugerencias, abre un issue en el repositorio.

Proyecto para Penguin Academy 🐧🚀
