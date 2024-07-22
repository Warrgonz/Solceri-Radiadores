# routes/vacaciones.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.vacaciones import Vacaciones
from utils.db import db
from models.usuarios import Usuarios

vacaciones_bp = Blueprint('vacaciones', __name__)

@vacaciones_bp.route('/vacaciones')
def listar_vacaciones():
    # Aquí podrías listar las vacaciones actuales del usuario
    return render_template('vacaciones.html')

@vacaciones_bp.route('/vacaciones/nueva', methods=['GET', 'POST'])
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
        
        nueva_vacacion = Vacaciones(
            id_solicitante=user_id,
            estado="Pendiente",
            detalles=detalles,
            dia_inicio=dia_inicio,
            dia_final=dia_final
        )
        
        db.session.add(nueva_vacacion)
        db.session.commit()
        
        return redirect(url_for('vacaciones.listar_vacaciones', VacacionSolicitada_alert='success'))  # Redirige con parámetro de alerta
    
    return render_template('vacaciones_solicitud.html', user_name=user_name)

    """

    Nice to have:

    1. Buscador
    2. Cambiar el diseño a tabs, con eso vamos a tener las pestañas:

    - Activas
    - Calendario
    - Denegadas

    Vista del coolaborador:

    Va iniciar en el calendario donde va poder ver todas las solicitudes de vacaciones, y el estado de sus solicitudes. Then, este html de estados 
    va tener la información de la solicitud y la descripción y/o "comentario_solicitud" (Posible campo en db missing). Tener un btn atras! 

    """