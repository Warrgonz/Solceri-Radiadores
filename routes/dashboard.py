from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models.usuarios import Usuarios
from models.roles import Roles
from datetime import datetime
from utils.db import db
from utils.firebase import FirebaseUtils

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

@dashboard_bp.route('/perfil')
def perfil():
    # Verificar si hay un usuario en la sesión
    if 'user_id' in session:
        user_id = session.get('user_id')
        
        # Recuperar todos los datos del usuario desde la base de datos
        usuario = Usuarios.query.get(user_id)
        
        if usuario:
            # Imprimir los datos del usuario para depuración
            print("Datos del usuario:", usuario)
            
            # Pasar los datos del usuario al template
            return render_template('miPerfil.html', usuario=usuario)
        else:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('usuarios.login'))
    else:
        flash('No se ha iniciado sesión', 'danger')
        return redirect(url_for('usuarios.login'))
    
@dashboard_bp.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    user_id = session.get('user_id')
    if not user_id:
        flash('No se ha iniciado sesión', 'danger')
        return redirect(url_for('usuarios.login'))

    usuario = Usuarios.query.get_or_404(user_id)
    roles = Roles.query.all()

    if request.method == 'POST':
        try:
            # Capturar los cambios realizados
            if usuario.cedula != request.form['cedula']:
                usuario.cedula = request.form['cedula']

            if usuario.nombre != request.form['nombre']:
                usuario.nombre = request.form['nombre']

            if usuario.primer_apellido != request.form['primer_apellido']:
                usuario.primer_apellido = request.form['primer_apellido']

            if usuario.segundo_apellido != request.form['segundo_apellido']:
                usuario.segundo_apellido = request.form['segundo_apellido']

            # Validar y asignar Fecha_Contratacion
            fecha_contratacion = request.form.get('fecha_contratacion')
            print(f"Fecha de contratación recibida: {fecha_contratacion}")
            try:
                if fecha_contratacion:
                    usuario.Fecha_Contratacion = datetime.strptime(fecha_contratacion, '%Y-%m-%d').date()
                else:
                    usuario.Fecha_Contratacion = None
            except ValueError as ve:
                flash(f'Error en la fecha de contratación: {ve}', 'danger')
                return redirect(url_for('dashboard_bp.editar_perfil'))

            # Manejar la actualización de la imagen
            if 'ruta_imagen' in request.files:
                nueva_imagen = request.files['ruta_imagen']
                if nueva_imagen.filename != '':
                    # Subir la nueva imagen a Firebase con un nombre único
                    ruta_imagen = FirebaseUtils.update_image(nueva_imagen, usuario.ruta_imagen)
                    usuario.ruta_imagen = ruta_imagen

            # Guardar los cambios en la base de datos
            db.session.commit()

            flash(f'Perfil actualizado exitosamente.', 'success')
            return redirect(url_for('dashboard_bp.perfil'))
        except Exception as e:
            # Manejar el error y mostrar un mensaje al usuario
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {e}', 'danger')
            print(f"Detalles del error: {e}")
            return redirect(url_for('dashboard_bp.editar_perfil'))

    return render_template('usuarios_editar.html', usuario=usuario, roles=roles)

    
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