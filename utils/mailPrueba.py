import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar los datos necesarios para el correo electrónico
sender_email = "solceriforge@gmail.com"
password = os.getenv("PASSWORD_MAIL")
receiver_email = "Warren0419@outlook.com"
subject = "Asunto del correo"
body = """
<html>
<head></head>
<body>
    <h1 style="color:SlateGray;">¡Hola, Warren!</h1>
    <p>Este es un ejemplo de correo electrónico en formato HTML.</p>
    <table style="width:50%; border: 1px solid black;">
        <tr>
            <th style="border: 1px solid black; padding: 8px;">Nombre</th>
            <th style="border: 1px solid black; padding: 8px;">Cantidad</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Manzanas</td>
            <td style="border: 1px solid black; padding: 8px;">5</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Naranjas</td>
            <td style="border: 1px solid black; padding: 8px;">10</td>
        </tr>
    </table>
</body>
</html>
"""

# Crear el mensaje de correo electrónico
msg = EmailMessage()
msg.set_content(body, subtype='html')  # Establecer el cuerpo del mensaje como HTML
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

# Enviar el correo electrónico utilizando SMTP
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Habilitar el modo seguro (TLS)
        smtp.login(sender_email, password)
        smtp.send_message(msg)
        print("Correo electrónico enviado correctamente!")
except Exception as e:
    print(f"No se pudo enviar el correo electrónico. Error: {e}")
