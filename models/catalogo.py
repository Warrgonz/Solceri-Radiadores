from utils.db import db
from sqlalchemy import Integer, String, Text

class Catalogo(db.Model):
    __tablename__ = 'catalogo'
    id_catalogo = db.Column(Integer, primary_key=True, autoincrement=True)
    sku = db.Column(String(255), nullable=False)
    nombre_producto = db.Column(String(255), nullable=False)
    descripcion = db.Column(Text, nullable=True)
    precio = db.Column(db.Integer, nullable=True, default=0)
    ruta_imagen = db.Column(db.String(255), nullable=False)

    def __init__(self, sku, nombre_producto, descripcion, precio, ruta_imagen):
        self.sku = sku
        self.nombre_producto = nombre_producto
        self.descripcion = descripcion
        self.precio = precio if precio is not None else '0'
        self.ruta_imagen = ruta_imagen 

    def __repr__(self):
        return f'<Catalogo {self.sku} {self.nombre_producto} {self.descripcion}>'
