from flask_sqlalchemy import SQLAlchemy  # ORM para interactuar con la base de datos
from marshmallow import Schema, fields  # Para serialización/deserialización de datos

db = SQLAlchemy()  # Inicialización de la base de datos

# Modelo de usuario
class User(db.Model):
    __tablename__ = 'users_database'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)

# Esquema para serialización/deserialización de usuarios
class UserSchema(Schema):
    name = fields.Str()
    age = fields.Int()
    username = fields.Str()

user_schema = UserSchema()  # Instancia del esquema de usuario

