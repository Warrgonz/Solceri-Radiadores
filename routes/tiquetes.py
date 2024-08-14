from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from utils.db import db
from utils.auth import login_required, role_required
from models.usuarios import Usuarios
from models.grupos import Grupos
from models.categorias import Categorias
from models.tiquetes import Tiquetes
from models.tiquetes import Estados
from models.comentarios import Comentarios
from datetime import datetime
from utils.servicio_mail import send_email_async


tiquetes_bp = Blueprint('tiquetes', __name__)

@tiquetes_bp.route('/tiquetes')
def tiquetes_listar():
    tiquetes = Tiquetes.query.all()
    return render_template('tiquetes.html', tiquetes=tiquetes)

@tiquetes_bp.route('/tiquete/crear', methods=['GET', 'POST'])
def tiquete_crear():
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        grupo_asignado = request.form.get('grupo_asignado')
        trabajador_designado = request.form.get('trabajador_designado')
        categoria = request.form.get('categoria')
        resumen = request.form.get('resumen')
        descripcion = request.form.get('descripcion')
        direccion = request.form.get('direccion')
        id_estado = request.form.get('estado')
        fecha_asignacion = datetime.utcnow()  # Establecer la fecha de asignación actual

        nuevo_tiquete = Tiquetes(
            id_cliente=id_cliente,
            grupo_asignado=grupo_asignado,
            trabajador_designado=trabajador_designado,
            categoria=categoria,
            resumen=resumen,
            descripcion=descripcion,
            direccion=direccion,
            id_estado=id_estado,
            fecha_asignacion=fecha_asignacion  # Incluir la fecha de asignación
        )

        try:
            db.session.add(nuevo_tiquete)
            db.session.commit()
            flash('Tiquete creado exitosamente', 'success')
            return redirect(url_for('tiquetes.tiquetes_listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el tiquete: {str(e)}', 'danger')
            return redirect(url_for('tiquetes.tiquete_crear'))

    # Cargar datos necesarios para los selects
    clientes = Usuarios.query.filter_by(id_rol=3).all()  # Filtrar por rol de cliente
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()  # Admin y Colaboradores
    categorias = Categorias.query.all()
    estados = Estados.query.all()

    return render_template(
        'tiquete_crear.html',
        clientes=clientes,
        grupos=grupos,
        trabajadores=trabajadores,
        categorias=categorias,
        estados=estados,
        fecha_actual=datetime.utcnow()
    )

@tiquetes_bp.route('/tiquete/editar/<int:id>', methods=['GET', 'POST'])
def tiquete_editar(id):
    tiquete = Tiquetes.query.get_or_404(id)

    if request.method == 'POST':
        nuevo_cliente = request.form.get('id_cliente')
        nuevo_grupo = request.form.get('grupo_asignado')
        nuevo_trabajador = request.form.get('trabajador_designado')
        nuevo_categoria = request.form.get('categoria')
        nuevo_resumen = request.form.get('resumen')
        nuevo_descripcion = request.form.get('descripcion')
        nuevo_direccion = request.form.get('direccion')
        nuevo_estado = request.form.get('estado')

        # Captura los valores antiguos
        antiguo_cliente = tiquete.id_cliente
        antiguo_grupo = tiquete.grupo_asignado
        antiguo_trabajador = tiquete.trabajador_designado
        antiguo_categoria = tiquete.categoria
        antiguo_resumen = tiquete.resumen
        antiguo_descripcion = tiquete.descripcion
        antiguo_direccion = tiquete.direccion
        antiguo_estado = tiquete.id_estado

        # Actualizar los campos del tiquete
        tiquete.id_cliente = int(nuevo_cliente) if nuevo_cliente else None
        tiquete.grupo_asignado = int(nuevo_grupo) if nuevo_grupo else None
        tiquete.trabajador_designado = int(nuevo_trabajador) if nuevo_trabajador else None
        tiquete.categoria = int(nuevo_categoria) if nuevo_categoria else None
        tiquete.resumen = nuevo_resumen
        tiquete.descripcion = nuevo_descripcion
        tiquete.direccion = nuevo_direccion
        tiquete.id_estado = int(nuevo_estado) if nuevo_estado else None

        # Solo actualizar la fecha de asignación si el trabajador designado ha cambiado
        if antiguo_trabajador != tiquete.trabajador_designado:
            tiquete.fecha_asignacion = datetime.utcnow()

        # Comparar valores y agregar comentario si hay cambios
        comentarios = []
        if antiguo_cliente != tiquete.id_cliente:
            comentarios.append(f"Cliente: {get_nombre_cliente(antiguo_cliente)} ----> {get_nombre_cliente(tiquete.id_cliente)}")
        if antiguo_grupo != tiquete.grupo_asignado:
            comentarios.append(f"Grupo asignado: {get_nombre_grupo(antiguo_grupo)} ----> {get_nombre_grupo(tiquete.grupo_asignado)}")
        if antiguo_trabajador != tiquete.trabajador_designado:
            comentarios.append(f"Trabajador designado: {get_nombre_trabajador(antiguo_trabajador)} ----> {get_nombre_trabajador(tiquete.trabajador_designado)}")
        if antiguo_categoria != tiquete.categoria:
            comentarios.append(f"Categoría: {get_nombre_categoria(antiguo_categoria)} ----> {get_nombre_categoria(tiquete.categoria)}")
        if antiguo_resumen != tiquete.resumen:
            comentarios.append(f"Resumen: {antiguo_resumen} ----> {tiquete.resumen}")
        if antiguo_descripcion != tiquete.descripcion:
            comentarios.append(f"Descripción: {antiguo_descripcion} ----> {tiquete.descripcion}")
        if antiguo_direccion != tiquete.direccion:
            comentarios.append(f"Dirección: {antiguo_direccion} ----> {tiquete.direccion}")
        if antiguo_estado != tiquete.id_estado:
            comentarios.append(f"Estado: {get_nombre_estado(antiguo_estado)} ----> {get_nombre_estado(tiquete.id_estado)}")

        if comentarios:
            comentario_text = "<strong>Se realizaron los siguientes cambios:</strong> <br>" + "<br>".join(comentarios)
            user_id = session.get('user_id')
            usuario = Usuarios.query.filter_by(id_usuario=user_id).first()
            nombre_usuario = f"{usuario.nombre} {usuario.primer_apellido}"

            nuevo_comentario = Comentarios(
                id_tiquete=id,
                nombre_usuario=nombre_usuario,
                comentario=comentario_text
            )
        db.session.add(nuevo_comentario)

        try:
            db.session.commit()
            flash('Tiquete actualizado exitosamente', 'success')
            return redirect(url_for('tiquetes.tiquetes_listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el tiquete: {str(e)}', 'danger')
            return redirect(url_for('tiquetes.tiquete_editar', id=id))

    # Cargar datos necesarios para los selects
    clientes = Usuarios.query.filter_by(id_rol=3).all()  # Clientes
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()  # Admin y Colaboradores
    categorias = Categorias.query.all()
    estados = Estados.query.all()

    # Condición para mostrar comentarios según el rol del usuario

    user_id = session.get('user_id')
    usuario_sesion = Usuarios.query.filter_by(id_usuario=user_id).first()
    usuario_sesion_rol = usuario_sesion.id_rol

    # Filtrar comentarios según el rol del usuario en sesión
    if usuario_sesion_rol in [1, 2]:  # Admin o Colaborador
        comentarios = Comentarios.query.filter_by(id_tiquete=id).order_by(Comentarios.fecha_creacion.desc()).all()
    else:  # Cliente
        comentarios = Comentarios.query.filter_by(id_tiquete=id, visible_cliente=1).order_by(Comentarios.fecha_creacion.desc()).all()

    return render_template(
        'tiquete_editar.html',
        tiquete=tiquete,
        clientes=clientes,
        grupos=grupos,
        trabajadores=trabajadores,
        categorias=categorias,
        estados=estados,
        comentarios=comentarios,
        fecha_actual=datetime.utcnow()
    )


def get_nombre_cliente(id_cliente):
    cliente = Usuarios.query.get(id_cliente)
    return f"{cliente.nombre} {cliente.primer_apellido}" if cliente else "Desconocido"

def get_nombre_grupo(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    return grupo.nombre if grupo else "Desconocido"

def get_nombre_trabajador(id_trabajador):
    trabajador = Usuarios.query.get(id_trabajador)
    return f"{trabajador.nombre} {trabajador.primer_apellido}" if trabajador else "Desconocido"

def get_nombre_categoria(id_categoria):
    categoria = Categorias.query.get(id_categoria)
    return categoria.categoria if categoria else "Desconocida"

def get_nombre_estado(id_estado):
    estado = Estados.query.get(id_estado)
    return estado.estado if estado else "Desconocido"



@tiquetes_bp.route('/tiquete/eliminar/<int:id_tiquete>', methods=['POST'])
def eliminar_tiquete(id_tiquete):
    try:
        # Obtener el tiquete de la base de datos
        tiquete = Tiquetes.query.get(id_tiquete)
        
        if not tiquete:
            flash('Tiquete no encontrado', 'danger')
            return redirect(url_for('tiquetes.tiquetes_listar'))

        # Eliminar el tiquete de la base de datos
        db.session.delete(tiquete)
        db.session.commit()

        flash('Tiquete eliminado exitosamente', 'success')
    except Exception as e:
        # Manejo de excepciones
        print(f"Error al eliminar tiquete: {str(e)}")
        db.session.rollback()
        flash('Error al eliminar el tiquete', 'danger')
    
    return redirect(url_for('tiquetes.tiquetes_listar'))

# Ruta para agregar comentario
@tiquetes_bp.route('/tiquete/<int:id>/add_comment', methods=['POST'])
def add_comment(id):
    comentario_text = request.form.get('nota_interna')
    visible_cliente = request.form.get('visible_cliente') == 'on'  # Capturar el estado del checkbox

    if not comentario_text:
        flash('El comentario no puede estar vacío.', 'danger')
        return redirect(url_for('tiquetes.tiquete_detalle', id=id))

    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión para agregar un comentario.', 'danger')
        return redirect(url_for('auth.login'))

    # Se obtiene usuario en sesión
    usuario = Usuarios.query.filter_by(id_usuario=user_id).first()
    nombre_usuario = f"{usuario.nombre} {usuario.primer_apellido}"

    # Crear nuevo comentario
    nuevo_comentario = Comentarios(
        id_tiquete=id,
        nombre_usuario=nombre_usuario,
        comentario=comentario_text,
        visible_cliente=visible_cliente 
    )
    db.session.add(nuevo_comentario)
    db.session.commit()

    # Enviar correo al cliente si el comentario es visible para él
    if visible_cliente:
        # Obtener el cliente relacionado con el tiquete
        tiquete = Tiquetes.query.get(id)
        cliente = Usuarios.query.get(tiquete.id_cliente)

        if cliente and cliente.correo:
            subject = f"Se han agregado comentarios en tu tiquete (Ticket #{id})"
            body = f"""
            <html>
            <head></head>
            <body>
                <h1 style="color:SlateGray;">¡Hola {cliente.nombre}!</h1>
                <p>Se ha agregado un nuevo comentario en tu tiquete:</p>
                <p><strong>{comentario_text}</strong></p>
                <p>Puedes ver los detalles del tiquete haciendo clic <a href="http://127.0.0.1:5000/tiquete/editar/{id}">aquí</a>.</p>
            </body>
            </html>
            """
            send_email_async(cliente.correo, subject, body)

    flash('Comentario agregado exitosamente.', 'success')
    return redirect(url_for('tiquetes.tiquete_editar', id=id))
