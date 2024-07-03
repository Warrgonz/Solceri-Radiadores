# utils/servicio_mail.py

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import string
import secrets
import threading
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar los datos necesarios para el correo electrónico
sender_email = "solceriforge@gmail.com"
password = os.getenv("PASSWORD_MAIL")

def send_email(receiver_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body, subtype='html')  # Establecer el cuerpo del mensaje como HTML
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Habilitar el modo seguro (TLS)
            smtp.login(sender_email, password)
            smtp.send_message(msg)
            print(f"Correo electrónico enviado correctamente a {receiver_email}!")
    except Exception as e:
        print(f"No se pudo enviar el correo electrónico a {receiver_email}. Error: {e}")
        
def send_email_async(receiver_email, subject, body):
    email_thread = threading.Thread(target=send_email, args=(receiver_email, subject, body))
    email_thread.start()
        
def generate_temp_password():
    """Genera una contraseña temporal aleatoria."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))


def generate_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(user.correo, salt='password-reset-salt')

def send_reset_email(user, token):
    from flask import current_app  # Importar aquí para evitar importación circular

    with current_app.app_context():
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        reset_url = url_for('usuarios.reset_with_token', token=token, _external=True)
        subject = "Restablecer Contraseña"
        body = f"""
        <html>
        <head></head>
        <body>
            <h1 style="color:SlateGray;">¡Hola!</h1>
            <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
            <p><a href="{reset_url}">Restablecer Contraseña</a></p>
            <p>Si no solicitaste este cambio, por favor ignora este correo.</p>
        </body>
        </html>
        """
        send_email_async(user.correo, subject, body)