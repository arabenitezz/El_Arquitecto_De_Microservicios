from flask import Flask, request, jsonify  # Flask para crear la aplicación web
from models import db, AgeQueryResult  # Importa la base de datos y el modelo
import requests  # Para hacer peticiones HTTP
import jwt  # Para manejar tokens JWT
from functools import wraps  # Para crear decoradores
from circuitbreaker import circuit  # Para implementar el patrón circuit breaker
from tenacity import retry, stop_after_attempt, wait_fixed  # Para implementar reintentos

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos y la clave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ages_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key' 

# Inicialización de la base de datos con la app
db.init_app(app)

# Creación de las tablas en la base de datos
with app.app_context():
    db.create_all()

# Ruta para recibir eventos del Microservicio 1
@app.route('/events', methods=['POST'])
def handle_event():
    event = request.json
    print(f"Evento recibido: {event}")
    if event["event"] == "UserCreated":
        user_data = event["user"]
        # Guardar los datos del usuario en la base de datos local
        query_result = AgeQueryResult(user_id=user_data['id'], age=user_data['age'])
        db.session.add(query_result)
        db.session.commit()
        return jsonify({"message": "Los datos fueron sincronizados"}), 200
    return jsonify({"message": "Tipo de evento desconocido"}), 400

# Decorador para requerir token en las rutas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtiene el token del header de autorización
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None

        # Verifica si el token existe
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Decodifica el token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403
        
        # Llama a la función decorada con el ID del usuario actual
        return f(current_user_id, *args, **kwargs)
    
    return decorated

# Función para obtener datos del usuario con circuit breaker y reintentos
@circuit(failure_threshold=5, recovery_timeout=30)
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_user_data(user_id):
    # Hace una petición GET al servicio de usuarios
    response = requests.get(f'http://127.0.0.1:5001/users/{user_id}')
    response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
    return response.json()

# Ruta para obtener la edad del usuario
@app.route('/user_age', methods=['POST'])
@token_required
def get_user_age(current_user_id):
    try:
        # Obtiene y valida los datos de la petición
        data = request.get_json()
        if not data:
            return jsonify({"message": "No JSON data provided"}), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"message": "User ID is required"}), 400

        try:
            # Obtiene los datos del usuario
            user_data = get_user_data(user_id)
            age = user_data.get('age')

            # Guarda el resultado de la consulta en la base de datos
            query_result = AgeQueryResult(user_id=user_id, age=age)
            db.session.add(query_result)
            db.session.commit()

            # Retorna la edad del usuario
            return jsonify({"age": age}), 200
        except requests.exceptions.RequestException as e:
            # Maneja errores de la petición HTTP
            return jsonify({"message": "Error fetching user data", "error": str(e)}), 503

    except Exception as e:
        # Maneja cualquier otra excepción
        print("Exception:", str(e))
        return jsonify({"message": "Internal Server Error"}), 500

# Inicia el servidor
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5002)