# models/grupos.py
from utils.db import db

# Tabla miscelánea
grupo_usuario = db.Table('grupo_usuario',
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id_grupo'), primary_key=True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
)

class Grupos(db.Model):
    __tablename__ = 'grupos'
    id_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    # Tiempos personalizados en minutos
    on_time = db.Column(db.Integer)  # Tiempo máximo para On Time
    running_late = db.Column(db.Integer)  # Tiempo máximo para Running Late
    is_late = db.Column(db.Integer)  # Tiempo máximo para Is Late
    
    # Relación con usuarios
    usuarios = db.relationship('Usuarios', secondary=grupo_usuario, backref=db.backref('grupos', lazy='dynamic'))

    def __init__(self, nombre, descripcion, on_time, running_late, is_late):
        self.nombre = nombre
        self.descripcion = descripcion
        self.on_time = on_time
        self.running_late = running_late
        self.is_late = is_late