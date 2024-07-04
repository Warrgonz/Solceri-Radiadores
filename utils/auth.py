#utils/auth.py

from flask import session, redirect, url_for, flash
from functools import wraps
from models.usuarios import Usuarios

def login_required(func):
    """Decorador para verificar si el usuario ha iniciado sesión."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('usuarios.login'))  # Redirige a la página de inicio de sesión si no hay sesión activa
    return wrapper

def role_required(allowed_roles):
    """Decorador para verificar si el usuario tiene el rol adecuado."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' in session:
                # Obtiene el usuario desde la sesión
                user_id = session['user_id']
                user = Usuarios.query.get(user_id)

                if user:
                    # Obtiene el id del rol del usuario
                    user_role_id = user.id_rol if user.id_rol else None

                    # Verifica si el usuario tiene el id del rol adecuado
                    if user_role_id in allowed_roles:
                        return func(*args, **kwargs)
                    else:
                        flash('No tienes permisos para acceder a esta página.', 'danger')
                        # Redirige a una página de acceso no autorizado (403)
                        return redirect(url_for('usuarios.acceso_denegado'))
                else:
                    flash('Usuario no encontrado.', 'danger')
                    return redirect(url_for('usuarios.acceso_denegado'))
            else:
                flash('Inicia sesión para acceder a esta página.', 'warning')
                return redirect(url_for('usuarios.login'))
        return wrapper
    return decorator
