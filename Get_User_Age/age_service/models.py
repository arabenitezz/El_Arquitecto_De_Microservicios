from flask_sqlalchemy import SQLAlchemy  # ORM para interactuar con la base de datos

db = SQLAlchemy()  # Inicialización de la base de datos

# Modelo para almacenar los resultados de las consultas de edad
class AgeQueryResult(db.Model):
    __tablename__ = 'age_database'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), nullable=False)
    age = db.Column(db.Integer, nullable=False)