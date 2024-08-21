# models/archivos.py
from utils.db import db

class Archivos(db.Model):
    __tablename__ = 'archivos'
    
    id_archivo = db.Column(db.Integer, primary_key=True)
    tiquete_id = db.Column(db.String(50), db.ForeignKey('tiquetes.id_tiquete'), nullable=False)
    ruta_imagen = db.Column(db.String(255), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)  # Nuevo campo

    def __init__(self, tiquete_id, ruta_imagen, nombre_archivo):
        self.tiquete_id = tiquete_id
        self.ruta_imagen = ruta_imagen
        self.nombre_archivo = nombre_archivo
