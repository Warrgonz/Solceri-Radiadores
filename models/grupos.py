# models/grupos.py
from utils.db import db

class Grupos(db.Model):
    __tablename__ = 'grupos'
    id_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion