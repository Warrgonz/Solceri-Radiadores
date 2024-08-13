#__init__.py

from .grupos import grupos_bp
from .categorias import categorias_bp
from .usuarios import usuarios_bp
from .catalogo import catalogo_bp
from .index import inicio_bp
from .vacaciones import vacaciones_bp
from .tiquetes import tiquetes_bp
from .dashboard import dashboard_bp

blueprints = [
    grupos_bp,
    categorias_bp,
    usuarios_bp,
    catalogo_bp,
    inicio_bp,
    vacaciones_bp,
    tiquetes_bp,
    dashboard_bp
]