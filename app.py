# /app.py

from flask import Flask, session, g
from models.usuarios import Usuarios, create_admin_user
from models.roles import Roles
from routes import blueprints
from utils.db import init_db
import os
from dotenv import load_dotenv
from utils.config import Config
from models.cotizaciones import Cotizaciones
from models.mtl_cotizaciones import MtlCotizaciones

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

# Modo debug de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8080)
