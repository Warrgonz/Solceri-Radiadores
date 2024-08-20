from utils.db import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'
    id_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tiquete = db.Column(db.String(10), db.ForeignKey('tiquetes.id_tiquete'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad_productos = db.Column(db.Integer, nullable=False)
    archivo = db.Column(db.String(255), nullable=False)  # URL del archivo PDF en Firebase

    # Relaciones
    tiquete = db.relationship('Tiquetes', backref=db.backref('facturas', lazy=True))
    usuario = db.relationship('Usuarios', backref=db.backref('facturas', lazy=True))

    def __init__(self, id_tiquete, id_usuario, cantidad_productos, archivo):
        self.id_tiquete = id_tiquete
        self.id_usuario = id_usuario
        self.cantidad_productos = cantidad_productos
        self.archivo = archivo

    def __repr__(self):
        return f'<Factura #{self.id_factura} del Tiquete #{self.id_tiquete}>'
