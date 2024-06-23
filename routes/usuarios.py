from flask import Blueprint, render_template, request, url_for, redirect
from models.usuarios import Usuarios
from models.roles import Roles
from .firebase import FirebaseUtils
from utils.db import db

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
            ruta_imagen = request.files['ruta_imagen'] if 'ruta_imagen' in request.files else None
            id_rol = request.form['rol']
            fecha_contratacion = request.form['fecha_contratacion']
            
            # Procesa la imagen si está presente
            if ruta_imagen:
                ruta_imagen = FirebaseUtils.PostImagen(ruta_imagen)
            
            # Crear instancia del modelo de usuario
            nuevo_usuario = Usuarios(
                cedula=cedula,
                nombre=nombre,
                correo=correo,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                id_rol=id_rol,
                estado=True,
                Fecha_Contratacion=fecha_contratacion,
                ruta_imagen=ruta_imagen  # Asegúrate de que ruta_imagen esté definido en Usuarios
            )
            
            # Añadir el nuevo usuario a la sesión y guardar en la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()
            
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