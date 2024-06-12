from flask import Flask
from routes import blueprints
from utils.db import db
from sqlalchemy.exc import OperationalError
from sqlalchemy import text 

app = Flask(__name__)

# Configuración de la base de datos antes de inicializar SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/solceri'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy con la aplicación
db.init_app(app)

try:
    # Intentar realizar una consulta simple
    with app.app_context():
        db.session.execute(text("SELECT 1"))
        db.session.commit()
    
    # Si la consulta se ejecuta sin errores, mostrar el mensaje
    print("Conexión a la base de datos establecida")
except OperationalError as e:
    # Si hay un error en la consulta, imprimir el mensaje de error
    print("Error al conectar a la base de datos:", str(e))

# Registrar blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=8080)




