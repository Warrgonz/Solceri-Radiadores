from utils.db import db
from models.catalogo import Catalogo  # Importamos Catalogo aquí
from models.cotizaciones import Cotizaciones  # Asegúrate de importar Cotizaciones aquí

class MtlCotizaciones(db.Model):
    __tablename__ = 'mtl_cotizaciones'
    id_cotizacionTiquete = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cotizacion = db.Column(db.Integer, db.ForeignKey('cotizaciones.id_cotizacion'), nullable=False)
    id_catalogo = db.Column(db.Integer, db.ForeignKey('catalogo.id_catalogo'), nullable=False)
    producto = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer, nullable=True)

    # Relaciones
    catalogo = db.relationship('Catalogo', backref=db.backref('mtl_cotizaciones', lazy=True))
    cotizacion = db.relationship('Cotizaciones', back_populates='items')

    def __init__(self, id_catalogo, producto, cantidad, id_cotizacion):
        self.id_catalogo = id_catalogo
        self.producto = producto
        self.cantidad = cantidad
        self.id_cotizacion = id_cotizacion

    def __repr__(self):
        return f'<MtlCotizacion #{self.id_cotizacionTiquete}>'
