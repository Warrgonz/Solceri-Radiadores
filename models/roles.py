from utils.db import db

class Roles(db.Model):
    id_rol = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    
    def __init__(self, rol, descripcion):
        self.rol = rol
        self.descripcion = descripcion
