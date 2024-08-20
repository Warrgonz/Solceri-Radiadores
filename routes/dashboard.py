from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models.usuarios import Usuarios
from models.roles import Roles
from datetime import datetime
from utils.db import db
from utils.firebase import FirebaseUtils
from models.tiquetes import Tiquetes
from models.estados import Estados
from models.grupos import Grupos

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    
    if user_id:
        user = Usuarios.query.get(user_id)
        if user:
            user_role = user.id_rol
            
            if user_role == 3:
                # Si es cliente, solo puede ver los tiquetes donde es el cliente
                todos_los_tiquetes = Tiquetes.query.filter_by(id_cliente=user.id_usuario)\
                                                    .order_by(Tiquetes.fecha_asignacion.asc()).all()
                
                # No se requieren otros filtros ni se muestran otros tabs
                return render_template('dashboard.html',
                                       user_role=user_role,
                                       nombre_usuario=user.nombre,
                                       todos_los_tiquetes=todos_los_tiquetes)
            
            else:
                # Para otros roles, se muestran todos los tiquetes y filtrados por estado
                todos_los_tiquetes = Tiquetes.query.order_by(Tiquetes.fecha_asignacion.asc()).all()
                
                # Filtrar tiquetes asignados al usuario actual
                tiquetes_asignados = Tiquetes.query.filter_by(trabajador_designado=user.id_usuario).all()

                # Filtrar tiquetes por estado
                tiquetes_en_progreso = Tiquetes.query.join(Estados).filter(Estados.estado == 'En progreso')\
                                                     .order_by(Tiquetes.fecha_asignacion.asc()).all()
                tiquetes_en_espera = Tiquetes.query.join(Estados).filter(Estados.estado == 'En espera')\
                                                     .order_by(Tiquetes.fecha_asignacion.asc()).all()
                tiquetes_llamar_cliente = Tiquetes.query.join(Estados).filter(Estados.estado == 'Llamar cliente')\
                                                         .order_by(Tiquetes.fecha_asignacion.asc()).all()
                tiquetes_en_camino = Tiquetes.query.join(Estados).filter(Estados.estado == 'En camino')\
                                                     .order_by(Tiquetes.fecha_asignacion.asc()).all()

                return render_template('dashboard.html',
                                       user_role=user_role,
                                       nombre_usuario=user.nombre,
                                       todos_los_tiquetes=todos_los_tiquetes,
                                       tiquetes_asignados=tiquetes_asignados,
                                       tiquetes_en_progreso=tiquetes_en_progreso,
                                       tiquetes_en_espera=tiquetes_en_espera,
                                       tiquetes_llamar_cliente=tiquetes_llamar_cliente,
                                       tiquetes_en_camino=tiquetes_en_camino)
                
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
    
@dashboard_bp.route('/perfil/editar/<int:id>', methods=['GET', 'POST'])
def usuarios_editar(id):
    usuario = Usuarios.query.get_or_404(id)
    roles = Roles.query.all()
    user_id = session.get('user_id')

    usuario_id = Usuarios.query.filter_by(id_usuario=user_id).first()

    if usuario_id:
        rol_usuario_sesion = usuario_id.id_rol
    else:
        rol_usuario_sesion = None

    if request.method == 'POST':
        try:
            # Capturar los cambios realizados
            usuario.cedula = request.form['cedula']
            usuario.nombre = request.form['nombre']
            usuario.primer_apellido = request.form['primer_apellido']
            usuario.segundo_apellido = request.form['segundo_apellido']

            # Validar y asignar Fecha_Contratacion
            fecha_contratacion = request.form.get('fecha_contratacion')
            if fecha_contratacion:
                usuario.Fecha_Contratacion = datetime.strptime(fecha_contratacion, '%Y-%m-%d').date()
            else:
                usuario.Fecha_Contratacion = None

            # Actualizar el rol del usuario si ha cambiado
            usuario.id_rol = int(request.form['rol'])

            # Manejar la actualización de la imagen
            nueva_imagen = request.files.get('ruta_imagen')
            if nueva_imagen and nueva_imagen.filename != '':
                # Subir la nueva imagen a Firebase
                ruta_imagen = FirebaseUtils.update_image(nueva_imagen, usuario.ruta_imagen)
                if ruta_imagen:
                    usuario.ruta_imagen = ruta_imagen  # Actualizar la URL de la imagen en la base de datos

            # Guardar los cambios en la base de datos
            db.session.commit()

            flash(f'Usuario con cédula {usuario.cedula} modificado exitosamente.', 'success')
            return redirect(url_for('dashboard.perfil', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {e}', 'danger')
            return redirect(url_for('dashboard.usuarios_editar', id=id))

    return render_template('usuarios_editpublic.html', usuario=usuario, roles=roles, rol_usuario_sesion=rol_usuario_sesion)



    
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
    
@dashboard_bp.route('/404')
def error404():
    return render_template('404.html')

@dashboard_bp.route('/403')
def error403():
    return render_template('403.html')
