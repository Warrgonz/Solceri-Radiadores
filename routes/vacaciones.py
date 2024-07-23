# routes/vacaciones.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.vacaciones import Vacaciones
from utils.db import db
from models.usuarios import Usuarios
from models.roles import Roles
from utils.servicio_mail import send_email_async
from datetime import datetime
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

