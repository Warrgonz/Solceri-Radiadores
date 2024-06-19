from .equipos import equipos_bp
from .categorias import categorias_bp
from .usuarios import usuarios_bp
from .roles import roles_bp

blueprints = [
    equipos_bp,
    categorias_bp,
    usuarios_bp,
    roles_bp
]