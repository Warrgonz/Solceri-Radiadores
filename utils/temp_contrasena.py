# utils/temp_contrasena.py

import random
import string

# 8-10 caracteres y letras (mayúsculas y minúsculas), números y caracteres especiales (como @, #, $, ¡ o*).

def generar_contraseña_temporal(length=10):
    caracteres = string.ascii_letters + string.digits + "@#$!*"
    return ''.join(random.choice(caracteres) for _ in range(length))

