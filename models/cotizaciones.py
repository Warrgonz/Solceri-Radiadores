from utils.db import db
from datetime import datetime
from models.tiquetes import Tiquetes
from models.usuarios import Usuarios  # Importar el modelo Usuarios

class Cotizaciones(db.Model):
    __tablename__ = 'cotizaciones'
    id_cotizacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tiquete = db.Column(db.String(10), db.ForeignKey('tiquetes.id_tiquete'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)  # Nuevo campo para el usuario
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(255))

    # Relaciones
    tiquete = db.relationship('Tiquetes', backref=db.backref('cotizaciones', lazy=True))
    usuario = db.relationship('Usuarios', backref=db.backref('cotizaciones', lazy=True))  
    items = db.relationship('MtlCotizaciones', back_populates='cotizacion')

    def __init__(self, id_tiquete, id_usuario, fecha_creacion=None):
        self.id_tiquete = id_tiquete
        self.id_usuario = id_usuario  # Asignar el usuario que realizó la cotización
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.utcnow()

    def __repr__(self):
        return f'<Cotizacion #{self.id_cotizacion} por Usuario #{self.id_usuario}>'
