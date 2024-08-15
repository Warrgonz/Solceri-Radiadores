# routes/usuarios.py

from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify, session, current_app, make_response
from datetime import datetime
from models.usuarios import Usuarios
from models.roles import Roles
from utils.firebase import FirebaseUtils
from utils.db import db
from utils.servicio_mail import generate_temp_password, send_email_async, generate_reset_token, verify_reset_token
from utils.auth import login_required, role_required
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios')
@login_required
@role_required([1])
def usuarios():
    usuarios = Usuarios.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
@role_required([1])
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
            imagen_default = "https://firebasestorage.googleapis.com/v0/b/solceri-1650a.appspot.com/o/logoSolceri.png?alt=media&token=ae59e640-bba6-40f4-bce9-acb89c01d47f"
            if 'ruta_imagen' in request.files:
                ruta_imagen = request.files['ruta_imagen']
                if ruta_imagen.filename != '':
                    # Subir la nueva imagen a Firebase con un nombre único
                    ruta_imagen = FirebaseUtils.post_image(ruta_imagen)
                else:
                    ruta_imagen = imagen_default  # Usar imagen por defecto si no se selecciona ninguna imagen
            else:
                ruta_imagen = imagen_default  # Usar imagen por defecto si no se sube ninguna imagen

            id_rol = request.form['rol']
            fecha_contratacion = request.form.get('fecha_contratacion')
            
            # Validaciones
            if len(cedula) < 8:
                flash('La cédula debe tener al menos 8 dígitos.', 'danger')
                return redirect(request.url)
            
            if Usuarios.query.filter_by(cedula=cedula).first():
                flash('Ya existe un usuario con esta cédula.', 'danger')
                return redirect(request.url)
            
            if correo and Usuarios.query.filter_by(correo=correo).first():
                flash('Ya existe un usuario con este correo electrónico.', 'danger')
                return redirect(request.url)
            
            # Genera contraseña temporal
            temp_password = generate_temp_password()
            
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
            db.session.rollback()
            
            # Puedes renderizar nuevamente el formulario con un mensaje de error
            roles = Roles.query.all()
            return render_template('usuarios_crear.html', roles=roles)

    # Si es GET, simplemente renderiza el formulario para crear usuarios
    roles = Roles.query.all()
    return render_template('usuarios_crear.html', roles=roles)

@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required([1])
def usuarios_editar(id):
    usuario = Usuarios.query.get_or_404(id)
    roles = Roles.query.all()
    user_id = session.get('user_id') 

    # Verificar si el usuario está en la base de datos
    usuario_id = Usuarios.query.filter_by(id_usuario=user_id).first()

    # Asegurarse de que el usuario_id existe antes de acceder a id_rol
    if usuario_id:
        rol_usuario_sesion = usuario_id.id_rol
    else:
        rol_usuario_sesion = None

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
                return redirect(url_for('usuarios.usuarios_editar', id=id))

            # Actualizar el rol del usuario si ha cambiado
            if usuario.id_rol != int(request.form['rol']):
                usuario.id_rol = int(request.form['rol'])

            # Manejar la actualización de la imagen
            if 'ruta_imagen' in request.files:
                nueva_imagen = request.files['ruta_imagen']
                if nueva_imagen.filename != '':
                    # Subir la nueva imagen a Firebase con un nombre único
                    ruta_imagen = FirebaseUtils.update_image(nueva_imagen, usuario.ruta_imagen)
                    usuario.ruta_imagen = ruta_imagen

            # Guardar los cambios en la base de datos
            db.session.commit()

            flash(f'Usuario con cédula {usuario.cedula} modificado exitosamente.', 'success')
            return redirect(url_for('usuarios.usuarios'))
        except Exception as e:
            # Manejar el error y mostrar un mensaje al usuario
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {e}', 'danger')
            print(f"Detalles del error: {e}")
            return redirect(url_for('usuarios.usuarios_editar', id=id))

    return render_template('usuarios_editar.html', usuario=usuario, roles=roles, rol_usuario_sesion=rol_usuario_sesion)

@usuarios_bp.route('/usuarios/desactivar/<int:id>', methods=['POST'])
@login_required
@role_required([1])
def desactivar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    if usuario:
        usuario.estado = False
        db.session.commit()

        # Enviar correo electrónico de notificación
        subject = "Tu cuenta ha sido inactivada"
        body = f"""
        <html>
        <head></head>
        <body>
            <h1 style="color:SlateGray;">Cuenta Inactivada</h1>
            <p>Tu cuenta ha sido inactivada por un administrador.</p>
            <p>Si crees que esto es un error, por favor contacta con el soporte.</p>
        </body>
        </html>
        """
        send_email_async(usuario.correo, subject, body)
        
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404


@usuarios_bp.route('/usuarios/activar/<int:id>', methods=['POST'])
@login_required
@role_required([1])
def activar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    if usuario:
        usuario.estado = True
        db.session.commit()

        # Enviar correo electrónico de notificación
        subject = "Tu cuenta ha sido activada"
        body = f"""
        <html>
        <head></head>
        <body>
            <h1 style="color:SlateGray;">Cuenta Activada</h1>
            <p>Tu cuenta ha sido activada exitosamente. Ahora puedes iniciar sesión con tu correo y contraseña.</p>
            <p>Si necesitas asistencia, contactenos.</p>
        </body>
        </html>
        """
        send_email_async(usuario.correo, subject, body)

        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404

    
@usuarios_bp.route('/usuarios/eliminar/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
@role_required([1])
def eliminar_usuario(id_usuario):
    try:
        # Obtener el usuario de la base de datos
        usuario = Usuarios.query.get(id_usuario)
        
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('usuarios.usuarios'))

        # Eliminar el usuario de la base de datos
        db.session.delete(usuario)
        db.session.commit()

        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        # Manejo de excepciones
        print(f"Error al eliminar usuario: {str(e)}")
        db.session.rollback()
        flash('Error al eliminar el usuario', 'danger')
    
    return redirect(url_for('usuarios.usuarios'))

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():

    if 'user_id' in session:
        # Redirige al dashboard o a la página principal
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = 'remember_me' in request.form

        user = Usuarios.query.filter_by(correo=email).first()

        if user:
            # Verifica si el usuario está activo
            if not user.estado:
                return jsonify({'alert_type': 'error', 'alert_message': 'Tu cuenta está inactiva. Contacta al administrador.'}), 403
            
            # Verifica la contraseña
            if check_password_hash(user.contraseña, password):
                if user.contraseña_temp and check_password_hash(user.contraseña_temp, password):
                    session['user_id'] = user.id_usuario
                    response = make_response(jsonify({'redirect_url': url_for('usuarios.password_reset'), 'alert_type': 'warning', 'alert_message': 'Por favor, cambia tu contraseña temporal.'}))
                else:
                    session['user_id'] = user.id_usuario
                    response = make_response(jsonify({'redirect_url': url_for('usuarios.usuarios')}))

                if remember_me:
                    remember_token = user.generate_remember_token()
                    response.set_cookie('remember_token', remember_token, max_age=30*24*60*60)  # 30 days
                return response
            else:
                return jsonify({'alert_type': 'error', 'alert_message': 'Correo electrónico o contraseña incorrectos.'}), 401
        else:
            return jsonify({'alert_type': 'error', 'alert_message': 'Correo electrónico o contraseña incorrectos.'}), 401

    return render_template('login.html')


#Reset while logged

@usuarios_bp.route('/password_reset', methods=['GET', 'POST'])
@login_required
def password_reset():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = Usuarios.query.get(user_id)
        
        if user:
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            
            # Verificación de la contraseña actual
            if not user.check_password(current_password):
                return jsonify({'status': 'error', 'message': 'La contraseña actual es incorrecta.'})
            
            # Verificación de coincidencia entre nueva contraseña y su confirmación
            if new_password != confirm_password:
                return jsonify({'status': 'error', 'message': 'Las contraseñas no coinciden.'})
            
            # Verificación de longitud de la nueva contraseña
            if len(new_password) < 8:
                return jsonify({'status': 'error', 'message': 'La contraseña debe tener al menos 8 caracteres.'})

            try:
                # Actualización de la contraseña del usuario
                user.set_password(new_password)
                user.contraseña_temp = None  # Elimina la contraseña temporal, si existe
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Contraseña cambiada exitosamente.'})
            except Exception as e:
                db.session.rollback()  # Revertir en caso de error
                return jsonify({'status': 'error', 'message': f'Error al cambiar la contraseña: {str(e)}'})

        return jsonify({'status': 'error', 'message': 'Usuario no encontrado.'})
    
    return render_template('password_reset.html')


#Ruta para acceso denegado
@usuarios_bp.route('/403')
def acceso_denegado():
    return render_template('403.html'), 403

#Logout

@usuarios_bp.route('/logout')
@login_required
def logout():
    session.clear()  # Elimina todas las variables de sesión, incluido 'user_id'
    #flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('usuarios.login'))

#Metodos de recovery

#Reset request
@usuarios_bp.route('/password_recovery_request', methods=['GET', 'POST'])
def password_recovery_request():
    if request.method == 'POST':
        email = request.form['email']
        user = Usuarios.query.filter_by(correo=email).first()
        
        if user:
            token = generate_reset_token(email)
            reset_url = url_for('usuarios.password_recovery', token=token, _external=True)
            subject = "Solicitud de Restablecimiento de Contraseña"
            body = f"""
            <html>
            <head></head>
            <body>
                <h1 style="color:SlateGray;">Recuperación de Contraseña</h1>
                <p>Haga clic en el siguiente enlace para restablecer su contraseña:</p>
                <a href="{reset_url}">Restablecer Contraseña</a>
            </body>
            </html>
            """
            send_email_async(email, subject, body)
            return jsonify({'status': 'success', 'message': 'Hemos enviado exitosamente la solicitud para cambiar la contraseña. Revisa tu correo electrónico para restaurar tu contraseña.'})
        else:
            return jsonify({'status': 'error', 'message': 'No se encontró ninguna cuenta con ese correo electrónico.'})
    
    return render_template('password_recovery_request.html')


#Reset ya con token
@usuarios_bp.route('/password_recovery/<token>', methods=['GET', 'POST'])
def password_recovery(token):
    email = verify_reset_token(token)
    
    if not email:
        flash('El enlace de recuperación ha expirado o no es válido.', 'danger')
        return redirect(url_for('usuarios.login'))
    
    user = Usuarios.query.filter_by(correo=email).first()
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(request.url)
        
        if len(new_password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return redirect(request.url)

        try:
            user.set_password(new_password)
            db.session.commit()
            flash('Contraseña cambiada exitosamente.', 'success')
            return redirect(url_for('usuarios.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al cambiar la contraseña: {str(e)}', 'danger')
    
    return render_template('password_recovery.html')
