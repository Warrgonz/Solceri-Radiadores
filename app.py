from flask import Flask
from routes import blueprints
from utils.db import init_db
from utils.servicio_mail import MailConexion

app = Flask(__name__)

# Conexión a la base de datos
init_db(app)

# Configuración de Flask-Mail
mail = MailConexion(app)

# Registrar blueprints

for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Modo debug de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8080)




