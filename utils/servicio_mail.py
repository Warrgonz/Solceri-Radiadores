# utils/servicio_mail.py

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import string
import secrets
import threading
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app, url_for


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


#Funciones de forgot password

def generate_reset_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def verify_reset_token(token, expiration=3600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except Exception as e:
        return None
    return email