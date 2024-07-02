# routes/usuarios.py

from flask import Blueprint, render_template, request, url_for, redirect, flash
from models.usuarios import Usuarios
from models.roles import Roles
from .firebase import FirebaseUtils
from werkzeug.security import generate_password_hash
from utils.db import db
from utils.mail import generate_temp_password, send_temp_password_email


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
            
            # Envía correo electrónico con la contraseña temporal
            send_temp_password_email(nuevo_usuario.correo, temp_password)
            
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