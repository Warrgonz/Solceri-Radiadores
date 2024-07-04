from flask import Flask, session, g
from models.usuarios import Usuarios
from routes import blueprints
from utils.db import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexión a la base de datos
init_db(app)

@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = Usuarios.query.get(user_id)
        g.user = user
    else:
        g.user = None

# Configura una clave secreta personalizada
app.secret_key = os.getenv("PASSWORD_APP")

# Registrar blueprints

for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Modo debug de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8080)
