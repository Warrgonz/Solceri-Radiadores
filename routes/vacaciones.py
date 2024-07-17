from flask import Blueprint, render_template
from models.vacaciones import Vacaciones
from utils.db import db
#from utils.firebase import FirebaseUtils
#from utils.auth import login_required, role_required

vacaciones_bp = Blueprint('vacaciones', __name__)

@vacaciones_bp.route('/vacaciones')
def vacaciones():
    return render_template('vacaciones.html')

    """

    Pendiente:

    En la tabla de usuarios debería de agregar un campo de vacaciones disponibles, este campo simplemente llegará el admin a agregar el 
    dato y listo. Sin embargo, esto deberia de manejar el session para permitir solamente al administrador crear colaboradores. Es decir,
    colaboradores solamente va agregar clientes que estos clientes se van a usar para los tiquetes.

    Nice to have:

    1. Seria genial tener un dropdown para filtrar la tabla por rol, asi puedo ver un overview del objeto usuario mas preciso. 
    2. Cambiar el diseño a tabs, con eso vamos a tener las pestañas:

    - Planilla
    - Empleados
    - Calendario
    - Solicitudes archivadas

    Vista del coolaborador:

    Va iniciar en el calendario donde va poder ver todas las solicitudes de vacaciones, y el estado de sus solicitudes. Then, este html de estados 
    va tener la información de la solicitud y la descripción y/o "comentario_solicitud" (Posible campo en db missing). Tener un btn atras! 

    """