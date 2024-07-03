from flask import Flask
from routes import blueprints
from utils.db import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexión a la base de datos
init_db(app)

# Configura una clave secreta personalizada
app.secret_key = os.getenv("PASSWORD_APP")

# Registrar blueprints

for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Modo debug de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8080)
