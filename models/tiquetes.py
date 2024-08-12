#models/tiquetes.py

from utils.db import db
from models.usuarios import Usuarios  
from models.grupos import Grupos  
from models.categorias import Categorias
from models.estados import Estados
from datetime import datetime

from utils.db import db
from datetime import datetime

class Tiquetes(db.Model):
    __tablename__ = 'tiquetes'
    id_tiquete = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    grupo_asignado = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    trabajador_designado = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    resumen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)

    # Relaciones
    cliente = db.relationship('Usuarios', foreign_keys=[id_cliente])
    grupo = db.relationship('Grupos', backref=db.backref('tiquetes', lazy=True))
    trabajador = db.relationship('Usuarios', foreign_keys=[trabajador_designado])
    estado = db.relationship('Estados', backref=db.backref('tiquetes', lazy=True))
    categoria_rel = db.relationship('Categorias', backref=db.backref('tiquetes', lazy=True))

    def __init__(self, id_cliente, grupo_asignado, trabajador_designado, categoria, resumen, descripcion, direccion, id_estado):
        self.id_cliente = id_cliente
        self.grupo_asignado = grupo_asignado
        self.trabajador_designado = trabajador_designado
        self.categoria = categoria
        self.resumen = resumen
        self.descripcion = descripcion
        self.direccion = direccion
        self.id_estado = id_estado

    def __repr__(self):
        return f'<Tiquete #{self.id_tiquete}>'
    