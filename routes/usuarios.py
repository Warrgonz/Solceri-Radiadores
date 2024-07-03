# routes/usuarios.py

from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from models.usuarios import Usuarios
from models.roles import Roles
from .firebase import FirebaseUtils
from utils.db import db
from utils.servicio_mail import generate_temp_password, send_email_async

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios')
def usuarios():
    usuarios = Usuarios.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/crear', methods=['GET', 'POST'])
def usuarios_crear():
    if request.method == 'POST':
        try:
            # Procesa el formulario de creación de usuario
            cedula = request.form['id_empleado']
            correo = request.form.get('correo')
            nombre = request.form['nombre']
            primer_apellido = request.form['primer_apellido']
            segundo_apellido = request.form['segundo_apellido']
            ruta_imagen = None
            if 'ruta_imagen' in request.files:
                ruta_imagen = request.files['ruta_imagen']
                if ruta_imagen.filename != '':
                    ruta_imagen = FirebaseUtils.PostImagen(ruta_imagen)
                else:
                    ruta_imagen = None
            id_rol = request.form['rol']
            fecha_contratacion = request.form.get('fecha_contratacion')
            
            # Genera contraseña temporal
            temp_password = generate_temp_password()
            
            if Usuarios.query.filter_by(cedula=cedula).first():
                return jsonify({'existe': True})
            
            # Crea instancia del modelo de usuario
            nuevo_usuario = Usuarios(
                cedula=cedula,
                correo=correo,
                nombre=nombre,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                id_rol=id_rol,
                estado=True,
                Fecha_Contratacion=fecha_contratacion,
                ruta_imagen=ruta_imagen  # Asegúrate de que ruta_imagen esté definido en Usuarios
            )
            
            # Configura la contraseña temporal en el modelo de usuario
            nuevo_usuario.set_temp_password(temp_password)
            
            # Guarda el nuevo usuario en la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            # Envía correo electrónico con la contraseña temporal al nuevo usuario de forma asíncrona
            subject = "Contraseña Temporal"
            body = f"""
            <html>
            <head></head>
            <body>
                <h1 style="color:SlateGray;">¡Hola!</h1>
                <p>Tu contraseña temporal es: <strong>{temp_password}</strong></p>
                <p>Por favor, accede utilizando esta contraseña y cámbiala lo antes posible.</p>
            </body>
            </html>
            """
            send_email_async(correo, subject, body)
            
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('usuarios.usuarios'))
        
        except Exception as e:
            # Manejo de excepciones
            print(f"Error al crear usuario: {str(e)}")
            db.session.rollback()  # Revertir la sesión en caso de error
            
            # Puedes renderizar nuevamente el formulario con un mensaje de error
            roles = Roles.query.all()
            return render_template('usuarios_crear.html', roles=roles)

    # Si es GET, simplemente renderiza el formulario para crear usuarios
    roles = Roles.query.all()
    return render_template('usuarios_crear.html', roles=roles)

@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def usuarios_editar(id):
    usuario = Usuarios.query.get_or_404(id)
    roles = Roles.query.all()

    if request.method == 'POST':
        try:
            # Actualizar los campos del usuario con los datos del formulario
            usuario.cedula = request.form['cedula']
            usuario.nombre = request.form['nombre']
            usuario.primer_apellido = request.form['primer_apellido']
            usuario.segundo_apellido = request.form['segundo_apellido']
            usuario.correo = request.form['correo']
            usuario.rol_id = request.form['rol']
            usuario.fecha_contratacion = request.form.get('fecha_contratacion')

            # Guardar los cambios en la base de datos
            db.session.commit()

            flash(f'Usuario con cédula {usuario.cedula} modificado exitosamente.', 'success')
            return redirect(url_for('usuarios.usuarios'))
        except Exception as e:
            # Manejar el error y mostrar un mensaje al usuario
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {e}', 'danger')
            return redirect(url_for('usuarios.usuarios_editar', id=id))

    return render_template('usuarios_editar.html', usuario=usuario, roles=roles)

@usuarios_bp.route('/usuarios/desactivar/<int:id>', methods=['POST'])
def desactivar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    if usuario:
        usuario.estado = False
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404

@usuarios_bp.route('/usuarios/activar/<int:id>', methods=['POST'])
def activar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    if usuario:
        usuario.estado = True
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404



