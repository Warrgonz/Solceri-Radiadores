# models/grupos.py
from utils.db import db

# Tabla miselanea
grupo_usuario = db.Table('grupo_usuario',
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id_grupo'), primary_key=True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
)

class Grupos(db.Model):
    __tablename__ = 'grupos'
    id_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    
    # relacion con usuarios
    usuarios = db.relationship('Usuarios', secondary=grupo_usuario, backref=db.backref('grupos', lazy='dynamic'))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

