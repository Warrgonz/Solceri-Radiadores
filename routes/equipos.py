from flask import Blueprint, render_template

equipos_bp = Blueprint('equipos', __name__)

#Aqui todas las rutas para /equipos

@equipos_bp.route('/equipos')
def equipos():
    return render_template('equipos.html')