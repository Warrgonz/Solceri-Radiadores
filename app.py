# /app.py

from flask import Flask, session, g
from models.usuarios import Usuarios, create_admin_user
from models.roles import Roles
from models.estados import Estados
from routes import blueprints
from utils.db import init_db
import os
from dotenv import load_dotenv
from utils.config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config) 

# Conexión a la base de datos
init_db(app)

# Registrar blueprints

for blueprint in blueprints:
    app.register_blueprint(blueprint)

with app.app_context():
    create_admin_user()
    Roles.set_roles()
    Estados.set_estados()


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = Usuarios.query.get(user_id)
        if user:
            g.user = user
            g.user_role = user.id_rol  # Asegúrate de asignar el ID numérico del rol aquí
        else:
            g.user = None
            g.user_role = None
    else:
        g.user = None
        g.user_role = None

# Configura una clave secreta personalizada
app.secret_key = os.getenv("PASSWORD_APP")

# Modo debug de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8080)
