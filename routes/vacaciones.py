# routes/vacaciones.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.vacaciones import Vacaciones
from utils.db import db
from models.usuarios import Usuarios
from models.roles import Roles
from utils.servicio_mail import send_email_async
from datetime import datetime, date
from utils.auth import login_required, role_required
from math import ceil

vacaciones_bp = Blueprint('vacaciones', __name__)

@vacaciones_bp.route('/vacaciones')
@login_required
@role_required(allowed_roles=[1, 2])
def listar_vacaciones():
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión primero', 'danger')
        return redirect(url_for('usuarios.login'))

    user = Usuarios.query.get(user_id)
    if not user:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('usuarios.login'))

    entries = request.args.get('entries', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    dia_inicio = request.args.get('dia_inicio')
    dia_final = request.args.get('dia_final')
    estado = request.args.get('estado')

    # Construir la consulta base
    query = Vacaciones.query.filter_by(id_solicitante=user_id)

    # Aplicar filtros
    if dia_inicio:
        query = query.filter(Vacaciones.dia_inicio >= dia_inicio)
    if dia_final:
        query = query.filter(Vacaciones.dia_final <= dia_final)
    if estado:
        query = query.filter_by(estado=estado)

    solicitudes = query.paginate(page=page, per_page=entries, error_out=False)

    return render_template('vacaciones.html', solicitudes=solicitudes.items, user_role=user.rol.id_rol, entries=entries, page=page, total_pages=solicitudes.pages)

@vacaciones_bp.route('/vacaciones/calendarizacion', methods=['GET'])
def obtener_vacacion():

    # Access the query parameters
    start = request.args.get('start')
    end = request.args.get('end')

    # Print the received parameters
    print(f"Start: {start}, End: {end}")

    # Convert start and end to date objects if they are not already in the correct format
    try:
        start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
        end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # Query the database to get vacations within the specified range
    vacations = db.session.query(Vacaciones, Usuarios).join(Usuarios, Vacaciones.id_solicitante == Usuarios.id_usuario).filter(
        Vacaciones.estado == "Aprobado",
        Vacaciones.dia_inicio >= start_date,
        Vacaciones.dia_final <= end_date
    ).all()

    # Convert the query results to a list of dictionaries
    vacations_list = [{
        'id': vac.id_vacacion,
        'title': f"{user.nombre} {user.primer_apellido} {user.segundo_apellido}",
        'start': vac.dia_inicio.isoformat(),
        'end': vac.dia_final.isoformat()
    } for vac, user in vacations]

    return jsonify(vacations_list)


@vacaciones_bp.route('/vacaciones/info', methods=['GET'])
def info_vacacion():
    # Get the ID from the request arguments
    id = request.args.get('id')
    
    # Ensure ID is provided and is a valid integer
    if not id or not id.isdigit():
        return jsonify({'error': 'Invalid or missing ID'}), 400

    id = int(id)
    
    # Use aliases to distinguish between the two joins on the Usuarios table
    solicitante_alias = db.aliased(Usuarios)
    aprobador_alias = db.aliased(Usuarios)
    
    # Query the database to get vacation information along with requester and approver
    solicitud = db.session.query(Vacaciones, solicitante_alias, aprobador_alias).join(
        solicitante_alias, Vacaciones.id_solicitante == solicitante_alias.id_usuario
    ).join(
        aprobador_alias, Vacaciones.id_aprobador == aprobador_alias.id_usuario, isouter=True
    ).filter(
        Vacaciones.id_vacacion == id
    ).first_or_404()
    
    vac, solicitante, aprobador = solicitud

    # Create a dictionary from the solicitud object
    vacation_info = {
        'id_vacacion': vac.id_vacacion,
        'solicitante': {
            'nombre': solicitante.nombre,
            'primer_apellido': solicitante.primer_apellido,
            'segundo_apellido': solicitante.segundo_apellido
        },
        'aprobador': {
            'nombre': aprobador.nombre if aprobador else None,
            'primer_apellido': aprobador.primer_apellido if aprobador else None,
            'segundo_apellido': aprobador.segundo_apellido if aprobador else None
        },
        'estado': vac.estado,
        'detalles': vac.detalles,
        'dia_inicio': vac.dia_inicio.isoformat(),
        'dia_final': vac.dia_final.isoformat(),
        'fecha_solicitud': vac.fecha_solicitud.isoformat(),
        'dia_aprobacion': vac.dia_aprobacion.isoformat() if vac.dia_aprobacion else None
    }

    return jsonify(vacation_info)




@vacaciones_bp.route('/vacaciones/nueva', methods=['GET', 'POST'])
@login_required
@role_required(allowed_roles=[1, 2]) 
def nueva_vacacion():
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión primero', 'danger')
        return redirect(url_for('usuarios.login'))  # Redirige a la página de inicio de sesión si no hay usuario en sesión
    
    user = Usuarios.query.get(user_id)
    if not user:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('usuarios.login'))  # Redirige a la página de inicio de sesión si el usuario no existe
    
    user_name = f"{user.nombre} {user.primer_apellido} {user.segundo_apellido}"
    
    if request.method == 'POST':
        detalles = request.form.get('detalles')
        dia_inicio = request.form.get('dia_inicio')
        dia_final = request.form.get('dia_final')

        # Validar campos requeridos
        if not (detalles and dia_inicio and dia_final):
            flash('Todos los campos son requeridos.', 'danger')
            return redirect(url_for('vacaciones.nueva_vacacion'))
        
        # Validar fechas
        today = datetime.today().date()
        try:
            fecha_inicio = datetime.strptime(dia_inicio, '%Y-%m-%d').date()
            fecha_final = datetime.strptime(dia_final, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido.', 'danger')
            return redirect(url_for('vacaciones.nueva_vacacion'))

        if fecha_inicio < today:
            flash('La fecha de inicio debe ser de hoy en adelante.', 'danger')
            return redirect(url_for('vacaciones.nueva_vacacion'))
        
        if fecha_final <= fecha_inicio:
            flash('La fecha de finalización debe ser posterior a la fecha de inicio.', 'danger')
            return redirect(url_for('vacaciones.nueva_vacacion'))
        
        nueva_vacacion = Vacaciones(
            id_solicitante=user_id,
            estado="Pendiente",
            detalles=detalles,
            dia_inicio=dia_inicio,
            dia_final=dia_final
        )
        
        db.session.add(nueva_vacacion)
        db.session.commit()
        
        # Obtener todos los usuarios con rol de 'Administrador'
        admins = Usuarios.query.join(Roles).filter(Roles.rol == 'Administrador').all()
        for admin in admins:
            subject = "Nueva Solicitud de Vacaciones"
            body = f"""
            <html>
            <head></head>
            <body>
                <h1 style="color:SlateGray;">Nueva Solicitud de Vacaciones</h1>
                <p>El usuario {user.nombre} {user.primer_apellido} {user.segundo_apellido} ha solicitado vacaciones.</p>
                <p><strong>Fecha de Inicio:</strong> {dia_inicio}</p>
                <p><strong>Fecha de Finalización:</strong> {dia_final}</p>
                <p><strong>Detalles:</strong> {detalles}</p>
            </body>
            </html>
            """
            send_email_async(admin.correo, subject, body)
        
        flash('Solicitud de vacaciones enviada con éxito', 'success')
        return redirect(url_for('vacaciones.listar_vacaciones', VacacionSolicitada_alert='success'))  # Redirige a la lista de vacaciones
    
    return render_template('vacaciones_solicitud.html', user_name=user_name)

@vacaciones_bp.route('/vacaciones/detalle/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(allowed_roles=[1, 2]) 
def detalle_vacacion(id):
    solicitud = Vacaciones.query.get_or_404(id)
    solicitante = Usuarios.query.get(solicitud.id_solicitante)
    aprobador = Usuarios.query.get(solicitud.id_aprobador) if solicitud.id_aprobador else None

    return render_template("vacaciones_detalle.html", solicitud=solicitud, solicitante=solicitante, aprobador=aprobador)

@vacaciones_bp.route('/vacaciones/modificar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(allowed_roles=[1, 2]) 
def modificar_vacacion(id):
    solicitud = Vacaciones.query.get_or_404(id)
    solicitante = Usuarios.query.get(solicitud.id_solicitante)
    aprobador = Usuarios.query.get(solicitud.id_aprobador) if solicitud.id_aprobador else None

    if request.method == 'POST':
        dia_inicio = request.form.get('dia_inicio')
        dia_final = request.form.get('dia_final')
        detalles = request.form.get('detalles')

        # Validar campos requeridos
        if not (dia_inicio and dia_final and detalles):
            flash('Todos los campos son requeridos.', 'danger')
            return redirect(url_for('vacaciones.modificar_vacacion', id=id))

        # Validar fechas
        today = datetime.today().date()
        try:
            fecha_inicio = datetime.strptime(dia_inicio, '%Y-%m-%d').date()
            fecha_final = datetime.strptime(dia_final, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido.', 'danger')
            return redirect(url_for('vacaciones.modificar_vacacion', id=id))

        if fecha_inicio < today:
            flash('La fecha de inicio debe ser de hoy en adelante.', 'danger')
            return redirect(url_for('vacaciones.modificar_vacacion', id=id))

        if fecha_final < fecha_inicio:
            flash('La fecha de finalización debe ser posterior a la fecha de inicio.', 'danger')
            return redirect(url_for('vacaciones.modificar_vacacion', id=id))

        solicitud.dia_inicio = dia_inicio
        solicitud.dia_final = dia_final
        solicitud.detalles = detalles

        db.session.commit()
        
        # Enviar correo a todos los administradores
        admins = Usuarios.query.join(Roles).filter(Roles.rol == 'Administrador').all()
        for admin in admins:
            subject = "Modificación de Solicitud de Vacaciones"
            body = f"""
            <html>
            <head></head>
            <body>
                <h1 style="color:SlateGray;">Modificación de Solicitud de Vacaciones</h1>
                <p>El usuario {solicitante.nombre} {solicitante.primer_apellido} {solicitante.segundo_apellido} ha modificado su solicitud de vacaciones.</p>
                <p><strong>Fecha de Inicio:</strong> {dia_inicio}</p>
                <p><strong>Fecha de Finalización:</strong> {dia_final}</p>
                <p><strong>Detalles:</strong> {detalles}</p>
            </body>
            </html>
            """
            send_email_async(admin.correo, subject, body)

        flash('Solicitud de vacaciones modificada con éxito', 'success')
        return redirect(url_for('vacaciones.listar_vacaciones', VacacionModificada_alert='success'))

    return render_template("vacaciones_modificar.html", solicitud=solicitud, solicitante=solicitante, aprobador=aprobador)

@vacaciones_bp.route('/cancelar_solicitud', methods=['POST'])
def cancelar_solicitud():
    try:
        solicitud_id = request.form['solicitud_id']
        print(f"Solicitud ID: {solicitud_id}")

        solicitud = Vacaciones.query.get(solicitud_id)
        if solicitud:
            solicitante = Usuarios.query.get(solicitud.id_solicitante)
            if solicitante:
                # Eliminar la solicitud de la base de datos
                db.session.delete(solicitud)
                db.session.commit()
                print(f"Solicitud {solicitud_id} eliminada.")

                # Enviar correos a los administradores
                admins = Usuarios.query.join(Roles).filter(Roles.rol == 'Administrador').all()
                for admin in admins:
                    subject = "Cancelación de Solicitud de Vacaciones"
                    body = f"""
                    <html>
                    <head></head>
                    <body>
                        <h1 style="color:SlateGray;">Cancelación de Solicitud de Vacaciones</h1>
                        <p>El usuario {solicitante.nombre} {solicitante.primer_apellido} {solicitante.segundo_apellido} ha cancelado su solicitud de vacaciones.</p>
                        <p><strong>Fecha de Inicio:</strong> {solicitud.dia_inicio}</p>
                        <p><strong>Fecha de Finalización:</strong> {solicitud.dia_final}</p>
                        <p><strong>Detalles:</strong> {solicitud.detalles}</p>
                    </body>
                    </html>
                    """
                    send_email_async(admin.correo, subject, body)
                    print(f"Correo enviado a: {admin.correo}")

                return jsonify({'success': True, 'message': 'La solicitud ha sido eliminada.'})
            else:
                print(f"No se encontró el solicitante con ID: {solicitud.id_solicitante}")
                return jsonify({'success': False, 'message': 'No se encontró el solicitante.'})
        else:
            print(f"No se encontró la solicitud con ID: {solicitud_id}")
            return jsonify({'success': False, 'message': 'No se encontró la solicitud.'})
    except Exception as e:
        print(f"Error al eliminar la solicitud: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al eliminar la solicitud.'})





