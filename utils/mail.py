# utils/mail.py

from flask_mail import Message
from .servicio_mail import mail 
import string
import secrets

def send_temp_password_email(email, temp_password):
    """Envía un correo electrónico con la contraseña temporal al usuario."""
    try:
        # Configura el envío de correo electrónico aquí
        if mail:
            message = Message(
                subject='Contraseña Temporal',
                recipients=[email],
                body=f"Usuario: {email}\nContraseña temporal: {temp_password}"
            )
            mail.send(message)
            print(f"Correo electrónico enviado a {email} con la contraseña temporal.")
        else:
            print("No se pudo enviar el correo electrónico. 'mail' no está configurado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo electrónico: {str(e)}")

def generate_temp_password():
    """Genera una contraseña temporal aleatoria."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
