#models/tiquetes.py

from utils.db import db
from models.usuarios import Usuarios  
from models.grupos import Grupos  
from models.categorias import Categorias
from models.estados import Estados
from datetime import datetime

class Tiquetes(db.Model):
    __tablename__ = 'tiquetes'
    id_tiquete = db.Column(db.String(10), primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    grupo_asignado = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    trabajador_designado = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    resumen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime)
    fecha_finalizacion = db.Column(db.DateTime, default=None)


    # Relaciones
    cliente = db.relationship('Usuarios', foreign_keys=[id_cliente])
    grupo = db.relationship('Grupos', backref=db.backref('tiquetes', lazy=True))
    trabajador = db.relationship('Usuarios', foreign_keys=[trabajador_designado])
    estado = db.relationship('Estados', backref=db.backref('tiquetes', lazy=True))
    categoria_obj = db.relationship('Categorias', backref=db.backref('tiquetes', lazy=True))
    comentarios = db.relationship('Comentarios', back_populates='tiquete', cascade="all, delete-orphan")
    
    cotizaciones = db.relationship('Cotizaciones', back_populates='tiquete', cascade="all, delete-orphan", overlaps="cotizaciones,tiquete_ref")
    facturas = db.relationship('Factura', backref='tiquete_factura', cascade="all, delete-orphan", overlaps="facturas,tiquete_factura")
    reportes = db.relationship('Reportes', backref='tiquete', cascade="all, delete-orphan", lazy=True)

    def __init__(self, id_tiquete, id_cliente, grupo_asignado, trabajador_designado, categoria, resumen, descripcion, direccion, id_estado, fecha_asignacion, fecha_finalizacion=None):
        self.id_tiquete = id_tiquete
        self.id_cliente = id_cliente
        self.grupo_asignado = grupo_asignado
        self.trabajador_designado = trabajador_designado
        self.categoria = categoria
        self.resumen = resumen
        self.descripcion = descripcion
        self.direccion = direccion
        self.id_estado = id_estado
        self.fecha_asignacion = fecha_asignacion
        self.fecha_finalizacion = fecha_finalizacion

    def __repr__(self):
        return f'<Tiquete #{self.id_tiquete}>'


    