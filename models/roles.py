# models.roles.py

from utils.db import db

class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    
    def __init__(self, rol, descripcion):
        self.rol = rol
        self.descripcion = descripcion

    def __repr__(self):
        return f'<Role {self.rol}>'

        
        

