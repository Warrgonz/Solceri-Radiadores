from .grupos import grupos_bp
from .categorias import categorias_bp
from .usuarios import usuarios_bp

blueprints = [
    grupos_bp,
    categorias_bp,
    usuarios_bp,
]