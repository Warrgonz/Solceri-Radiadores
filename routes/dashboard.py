from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models.usuarios import Usuarios

dashboard_bp = Blueprint('dashboard', __name__)

# Funcionalidades para el usuario

@dashboard_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    
    if user_id:
        user = Usuarios.query.get(user_id)
        if user:
            user_role = user.id_rol  
            
            return render_template('dashboard.html', user_role=user_role , nombre_usuario=user.nombre)
    return render_template('dashboard.html')

# Funcionalidades para internos

@dashboard_bp.route('/test')
def test():
    # Verifica si el usuario está en sesión
    user_id = session.get('user_id')
    
    if user_id:
        # Obtiene el usuario de la base de datos
        user = Usuarios.query.get(user_id)
        
        if user:
            # Obtiene el rol del usuario
            user_role = user.rol.rol  # 'rol' es la relación, y 'rol' es el nombre del rol
            return jsonify({'role': user_role})
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    else:
        return jsonify({'error': 'No hay usuario en sesión'}), 401