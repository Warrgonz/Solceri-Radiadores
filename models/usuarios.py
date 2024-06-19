# models.usuarios.py

from utils.db import db
from models.roles import Roles  # Importar el modelo Roles para la relación

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula = db.Column(db.String(255), unique=True, nullable=False)
    correo = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    primer_apellido = db.Column(db.String(255))
    segundo_apellido = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    estado = db.Column(db.Boolean, default=False)
    ultima_actividad = db.Column(db.DateTime)
    Fecha_Contratacion = db.Column(db.Date)
    ruta_imagen = db.Column(db.String(255))
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))  # ForeignKey hacia roles.id_rol

    rol = db.relationship('Roles', backref=db.backref('usuarios', lazy=True))

    def __init__(self, cedula, correo, nombre=None, primer_apellido=None, segundo_apellido=None, id_rol=None, contraseña=None, estado=False, ultima_actividad=None, Fecha_Contratacion=None):
        self.cedula = cedula
        self.correo = correo
        self.nombre = nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.id_rol = id_rol
        self.contraseña = contraseña
        self.estado = estado
        self.ultima_actividad = ultima_actividad
        self.Fecha_Contratacion = Fecha_Contratacion

    def __repr__(self):
        return f'<Usuario {self.nombre} {self.primer_apellido}>'
