from utils.db import db
from models.cotizaciones import Cotizaciones  

class MtlCotizaciones(db.Model):
    __tablename__ = 'mtl_cotizaciones'
    id_cotizacionTiquete = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cotizacion = db.Column(db.Integer, db.ForeignKey('cotizaciones.id_cotizacion'), nullable=False)
    producto = db.Column(db.String(255), nullable=False) 
    cantidad = db.Column(db.String(255), nullable=False) 
    precio = db.Column(db.Integer, nullable=False) 

    # Relaciones
    cotizacion = db.relationship('Cotizaciones', back_populates='items')

    def __init__(self, producto, precio, cantidad, id_cotizacion):
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad  
        self.id_cotizacion = id_cotizacion

    def __repr__(self):
        return f'<MtlCotizacion #{self.id_cotizacionTiquete}>'



