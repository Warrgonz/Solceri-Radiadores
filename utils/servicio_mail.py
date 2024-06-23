# utils/mail.py

from flask_mail import Mail

mail = None  # Inicializado como None, se inicializará en MailConexion

def MailConexion(app):
    global mail
    try:
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Debes establecer tu dirección de correo aquí
        app.config['MAIL_PASSWORD'] = 'your_password'  # Debes establecer tu contraseña de correo aquí
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False

        mail = Mail(app)
        print("Mail connected successfully!")
        return mail

    except Exception as e:
        print(f"Error connecting to the mail server: {str(e)}")
        return None

# Exportar la instancia de Mail para que sea accesible desde otros módulos
__all__ = ['mail']
