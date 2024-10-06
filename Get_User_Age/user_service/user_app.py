from flask import request, Flask, jsonify # Para la aplicacion
from marshmallow import ValidationError # Manejo de errores
from models import db, user_schema, User
import jwt # Manejo de tokens jwt
import datetime # Para el tiempo de duracion de los tokens

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos y la clave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicialización de la base de datos con la app
db.init_app(app)

# Creación de las tablas en la base de datos
with app.app_context():
    db.create_all()

# Función para generar tokens JWT
def generate_token(user):
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    try:
        # Obtiene y valida los datos de la petición
        data = request.json
        validated_data = user_schema.load(data)

        # Crea un nuevo usuario
        new_user = User(
            name=validated_data['name'],
            age=validated_data['age'],
            username=validated_data['username']
        )
        # Guarda en la base de datos
        db.session.add(new_user)
        db.session.commit()

        # Genera un token para el nuevo usuario
        token = generate_token(new_user)

        # Retorna los datos del usuario y el token
        return jsonify({"user": user_schema.dump(new_user), "token": token}), 201

    except ValidationError as err:
        # Maneja errores de validación
        return jsonify(err.messages), 400
    except Exception as e:
        # Maneja cualquier otra excepción
        print("Exception:", str(e))
        return jsonify({"message": "Internal Server Error"}), 500

# Ruta para obtener los datos de un usuario
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Busca el usuario en la base de datos
        user = User.query.get(user_id)
        if user:
            # Si el usuario existe, retorna sus datos
            return jsonify(user_schema.dump(user)), 200
        else:
            # Si el usuario no existe, retorna un error
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        # Maneja cualquier excepción
        print("Exception:", str(e))
        return jsonify({"message": "Internal Server Error"}), 500

# Inicia el servidor
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)