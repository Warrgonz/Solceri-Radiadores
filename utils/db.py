from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app: Flask):
    try: # Cambiar contraseña de la db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/solceri'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        with app.app_context():
            db.create_all()  # Crear todas las tablas

        print("Database connected successfully!")
    
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")

