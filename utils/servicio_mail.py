from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# Configuración del servidor de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'warreno0419s@gmail.com'  # Reemplaza con tu dirección de correo Gmail
app.config['MAIL_PASSWORD'] = 'qtzt mirj gnzd jiwr'  # Reemplaza con la contraseña de tu cuenta Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'warreno0419s@gmail.com'  # Opcional: dirección predeterminada para enviar correos

# Inicialización de la extensión Flask-Mail
mail = Mail(app)
