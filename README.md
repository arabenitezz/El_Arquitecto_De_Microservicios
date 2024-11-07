# Get_Your_Age ! :)

# Microservices Project with Event Sourcing

Este proyecto implementa una arquitectura de microservicios utilizando Flask, con un patrón simplificado de Event Sourcing para la sincronización de datos entre servicios.

## Estructura del Proyecto

El proyecto consta de dos microservicios principales:

1. **User Service** (`user_app.py`): Maneja la creación y recuperación de usuarios.
2. **Age Service** (`age_app.py`): Maneja las consultas relacionadas con la edad de los usuarios.

Además, hay un archivo `models.py` compartido que define los modelos de datos para ambos servicios.

## Características

- Implementación de microservicios con Flask
- Uso de SQLAlchemy para ORM
- Autenticación mediante tokens JWT
- Patrón Event Sourcing simplificado para sincronización de datos
- Circuit Breaker y reintentos para manejo de fallos

## Requisitos

- Python 3.x
- Flask
- SQLAlchemy
- PyJWT
- Requests
- Circuit Breaker
- Tenacity

## Instalación

1. Clona este repositorio
2. Instala las dependencias:

```bash
pip install flask flask-sqlalchemy pyjwt requests circuitbreaker tenacity
```

## Configuración

Asegúrate de configurar las variables de entorno necesarias, especialmente la `SECRET_KEY` para la generación de tokens JWT.

## Ejecución

1. Inicia el User Service:

```bash
python user_app.py
```

2. En otra terminal, inicia el Age Service:

```bash
python age_app.py
```

## Uso

### Crear un nuevo usuario

POST /users
```json
{
  "name": "John Doe",
  "age": 30,
  "username": "johndoe"
}
```

### Obtener la edad de un usuario

POST /user_age
```json
{
  "user_id": "1"
}
```

## Event Sourcing

El proyecto utiliza un patrón simplificado de Event Sourcing:

1. Cuando se crea un usuario en el User Service, se genera un evento "UserCreated".
2. Este evento se envía al Age Service.
3. El Age Service almacena la información de edad del usuario para futuras consultas.

## Mejoras Futuras

- Implementar un sistema de mensajería más robusto (e.g., RabbitMQ, Kafka)
- Mejorar el manejo de errores y la resiliencia
- Agregar más pruebas unitarias y de integración

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos antes de hacer un pull request.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)
