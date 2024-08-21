from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from utils.db import db
from models.roles import Roles
from utils.auth import login_required, role_required
from models.usuarios import Usuarios
from models.grupos import Grupos
from models.categorias import Categorias
from models.tiquetes import Tiquetes
from models.tiquetes import Estados
from models.comentarios import Comentarios
from datetime import datetime, timedelta
from utils.servicio_mail import send_email_async
from models.facturas import Factura
from models.cotizaciones import Cotizaciones
from utils.firebase import FirebaseUtils
from models.archivos import Archivos


tiquetes_bp = Blueprint('tiquetes', __name__)

@tiquetes_bp.route('/tiquetes')
@login_required
def tiquetes_listar():
    user_id = session.get('user_id')
    user = Usuarios.query.get(user_id)
    user_role = user.id_rol

    #Sorted por fecha_asignacion
    if user_role == 3:
        # Cliente
        tiquetes = Tiquetes.query.filter_by(id_cliente=user_id)\
                                .order_by(Tiquetes.fecha_asignacion.asc()).all()
    elif user_role in [1, 2]:
        # User y Admin
        tiquetes = Tiquetes.query.order_by(Tiquetes.fecha_asignacion.asc()).all()
    else:
        # Else
        tiquetes = Tiquetes.query.order_by(Tiquetes.fecha_asignacion.asc()).all()

    return render_template('tiquetes.html', tiquetes=tiquetes, user_role=user_role, user_id=user_id)


@tiquetes_bp.route('/tiquete/detalles/<string:id>', methods=['GET'])
@login_required
def tiquete_detalles(id):
    tiquete = Tiquetes.query.get_or_404(id)

    # Cargar datos necesarios
    clientes = Usuarios.query.filter_by(id_rol=3).all()
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()
    categorias = Categorias.query.all()
    estados = Estados.query.all()
    categoria = Categorias.query.get(tiquete.categoria) if tiquete.categoria else None

    # Condición para mostrar comentarios según el rol del usuario

    user_id = session.get('user_id')
    usuario_sesion = Usuarios.query.filter_by(id_usuario=user_id).first()
    usuario_sesion_rol = usuario_sesion.id_rol

    # Filtrar comentarios según el rol del usuario en sesión
    if usuario_sesion_rol in [1, 2]:  # Admin o Colaborador
        comentarios = Comentarios.query.filter_by(id_tiquete=id).order_by(Comentarios.fecha_creacion.desc()).all()
    else:  # Cliente
        comentarios = Comentarios.query.filter_by(id_tiquete=id, visible_cliente=1).order_by(Comentarios.fecha_creacion.desc()).all()

    return render_template('tiquete_detalles.html', tiquete=tiquete, clientes=clientes, grupos=grupos,
                           trabajadores=trabajadores, categorias=categorias, estados=estados, comentarios=comentarios, categoria=categoria, usuario_sesion_rol=usuario_sesion_rol)


@tiquetes_bp.route('/tiquete/crear', methods=['GET', 'POST'])
@login_required
@role_required([1, 2])
def tiquete_crear():
    if request.method == 'POST':
        # Obtener datos del formulario
        id_cliente = request.form.get('id_cliente')
        grupo_asignado = request.form.get('grupo_asignado')
        trabajador_designado = request.form.get('trabajador_designado')
        categoria = request.form.get('categoria')
        resumen = request.form.get('resumen')
        descripcion = request.form.get('descripcion')
        direccion = request.form.get('direccion')
        id_estado = request.form.get('estado')
        fecha_asignacion = datetime.utcnow()
        fecha_asignacion = fecha_asignacion - timedelta(hours=6)

        nuevo_id_tiquete = generar_id_tiquete()

        nuevo_tiquete = Tiquetes(
            id_tiquete=nuevo_id_tiquete,
            id_cliente=id_cliente,
            grupo_asignado=grupo_asignado,
            trabajador_designado=trabajador_designado,
            categoria=categoria,
            resumen=resumen,
            descripcion=descripcion,
            direccion=direccion,
            id_estado=id_estado,
            fecha_asignacion=fecha_asignacion
        )

        # Manejar archivos adjuntos
        if 'archivos' in request.files:
            archivos = request.files.getlist('archivos')
            for archivo in archivos:
                if archivo and allowed_file(archivo.filename):
                    nombre_archivo = archivo.filename
                    url = FirebaseUtils.post_image(archivo)
                    if url:
                        nuevo_archivo = Archivos(tiquete_id=nuevo_id_tiquete, ruta_imagen=url, nombre_archivo=nombre_archivo)
                        db.session.add(nuevo_archivo)

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
    clientes = Usuarios.query.filter_by(id_rol=3).all()
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()
    categorias = Categorias.query.all()
    estados = Estados.query.filter(Estados.id_estado.notin_([6, 7])).all()

    fecha_actual=datetime.utcnow()
    fecha_actual = fecha_actual - timedelta(hours=6)

    return render_template(
        'tiquete_crear.html',
        clientes=clientes,
        grupos=grupos,
        trabajadores=trabajadores,
        categorias=categorias,
        estados=estados,
        fecha_actual=fecha_actual
    )

def generar_id_tiquete():
    # Obtener el último ID generado
    ultimo_tiquete = Tiquetes.query.order_by(Tiquetes.id_tiquete.desc()).first()
    
    if not ultimo_tiquete:
        return 'A0001'
    
    ultimo_id = ultimo_tiquete.id_tiquete
    letra = ultimo_id[0]
    numero = int(ultimo_id[1:]) + 1
    
    # Cambiar de letra si el número supera 9999
    if numero > 9999:
        letra = chr(ord(letra) + 1)
        numero = 1  # Reiniciar el número a 0001
    
    nuevo_id = f"{letra}{numero:04d}"
    return nuevo_id

def allowed_file(filename):
    allowed_extensions = {'pdf', 'doc', 'docx', 'png', 'jpg', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@tiquetes_bp.route('/tiquete/editar/<string:id>', methods=['GET', 'POST'])
@login_required
@role_required([1, 2])
def tiquete_editar(id):
    tiquete = Tiquetes.query.get_or_404(id)
    fecha_actual=datetime.utcnow()
    fecha_actual = fecha_actual - timedelta(hours=6)
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

        #TUKI WARREN
        if antiguo_trabajador != tiquete.trabajador_designado:
            #Variable fecha actual - fecha asignacion = (TIEMPO) --->>> Subir a tabla reportes
            #id usuario (Empleado), id_tiquete, datetime, TIEMPO, id usuario(cliente)?? opcional, o lo trae de tiqeute (STRING no ref)

            tiquete.fecha_asignacion = fecha_actual

        if int(nuevo_estado) in [6, 7]:
            tiquete.fecha_finalizacion = fecha_actual

        #ARCHIVOS
        if 'archivos' in request.files:
            archivos = request.files.getlist('archivos')
            for archivo in archivos:
                if archivo and allowed_file(archivo.filename):
                    url = FirebaseUtils.post_image(archivo)
                    nombre_archivo = archivo.filename
                    if url:
                        nuevo_archivo = Archivos(tiquete_id=id, ruta_imagen=url, nombre_archivo=nombre_archivo)
                        db.session.add(nuevo_archivo)    

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

            tiquete_actualizado = Tiquetes.query.get(id)
            cliente = Usuarios.query.get(tiquete_actualizado.id_cliente)
            if cliente and cliente.correo:
                subject = f"Actualización en tu tiquete (Ticket #{id})"
                body = f"""
                <html>
                <head></head>
                <body>
                    <h1 style="color:SlateGray;">¡Hola {cliente.nombre}!</h1>
                    <p>Se ha actualizado el estado de tu tiquete:</p>
                    <p><strong>Estado anterior:</strong> {get_nombre_estado(antiguo_estado)}</p>
                    <p><strong>Estado nuevo:</strong> {get_nombre_estado(tiquete_actualizado.id_estado)}</p>
                    <p>Puedes ver los detalles del tiquete haciendo clic <a href="https://solceri.com/tiquete/detalles/{id}">aquí</a>.</p>
                </body>
                </html>
                """
                send_email_async(cliente.correo, subject, body)

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
            db.session.add(nuevo_comentario)  # Añadir comentario solo si hay cambios

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

    # Obtener archivos asociados al tiquete
    archivos = Archivos.query.filter_by(tiquete_id=id).all()

    # Condición para mostrar comentarios según el rol del usuario

    user_id = session.get('user_id')
    usuario_sesion = Usuarios.query.filter_by(id_usuario=user_id).first()
    usuario_sesion_rol = usuario_sesion.id_rol
    # Obtener las facturas asociadas al tiquete
    facturas = Factura.query.filter_by(id_tiquete=id).all()

    # Filtrar comentarios según el rol del usuario en sesión
    if usuario_sesion_rol in [1, 2]:  # Admin o Colaborador
        comentarios = Comentarios.query.filter_by(id_tiquete=id).order_by(Comentarios.fecha_creacion.desc()).all()
    else:  # Cliente
        comentarios = Comentarios.query.filter_by(id_tiquete=id, visible_cliente=1).order_by(Comentarios.fecha_creacion.desc()).all()

    fecha_actual=datetime.utcnow()
    fecha_actual = fecha_actual - timedelta(hours=6)

    return render_template(
        'tiquete_editar.html',
        tiquete=tiquete,
        clientes=clientes,
        grupos=grupos,
        trabajadores=trabajadores,
        categorias=categorias,
        estados=estados,
        facturas=facturas, 
        comentarios=comentarios,
        archivos=archivos,
        fecha_actual=fecha_actual,
        usuario_sesion_rol = usuario_sesion_rol
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



@tiquetes_bp.route('/tiquete/eliminar/<string:id_tiquete>', methods=['POST'])
@login_required
@role_required([1, 2])
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
@tiquetes_bp.route('/tiquete/<string:id>/add_comment', methods=['POST'])
@login_required
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

        if cliente and cliente.correo and cliente.id_usuario != user_id:
            subject = f"Se han agregado comentarios en tu tiquete (Ticket #{id})"
            body = f"""
            <html>
            <head></head>
            <body>
                <h1 style="color:SlateGray;">¡Hola {cliente.nombre}!</h1>
                <p>Se ha agregado un nuevo comentario en tu tiquete:</p>
                <p><strong>{comentario_text}</strong></p>
                <p>Puedes ver los detalles del tiquete haciendo clic <a href="https://solceri.com/tiquete/detalles/{id}">aquí</a>.</p>
            </body>
            </html>
            """
            send_email_async(cliente.correo, subject, body)

    flash('Comentario agregado exitosamente.', 'success')
    redirect_url = request.form.get('redirect_url', 'tiquetes.tiquete_detalles')
    return redirect(url_for(redirect_url, id=id))
