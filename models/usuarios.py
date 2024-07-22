# models/usuarios.py

from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula = db.Column(db.String(255), unique=True, nullable=False)
    correo = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    primer_apellido = db.Column(db.String(255))
    segundo_apellido = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    contraseña_temp = db.Column(db.String(255))  # Añadir el campo para la contraseña temporal
    estado = db.Column(db.Boolean, default=False)
    ultima_actividad = db.Column(db.DateTime)
    Fecha_Contratacion = db.Column(db.Date, nullable=True)
    ruta_imagen = db.Column(db.String(255))  # Añade el campo ruta_imagen si es necesario
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))

    rol = db.relationship('Roles', backref=db.backref('usuarios', lazy=True))

    def __init__(self, cedula, correo, nombre=None, primer_apellido=None, segundo_apellido=None, id_rol=None, contraseña=None, contraseña_temp=None, estado=False, ultima_actividad=None, Fecha_Contratacion=None, ruta_imagen=None):
        self.cedula = cedula
        self.correo = correo
        self.nombre = nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.id_rol = id_rol
        self.contraseña = generate_password_hash(contraseña) if contraseña else None
        self.contraseña_temp = generate_password_hash(contraseña_temp) if contraseña_temp else None
        self.estado = estado
        self.ultima_actividad = ultima_actividad 
        self.Fecha_Contratacion = Fecha_Contratacion if Fecha_Contratacion else None
        self.ruta_imagen = ruta_imagen 
        
        # Configura la contraseña principal si se proporcionó una contraseña temporal
        if contraseña_temp:
            self.set_password(contraseña_temp)

    def __repr__(self):
        return f'<Usuario {self.nombre} {self.primer_apellido}>'
    
    def set_password(self, password):
        """Establece la contraseña principal."""
        if password:
            self.contraseña = generate_password_hash(password)

    def set_temp_password(self, temp_password):
        """Establece la contraseña temporal."""
        if temp_password:
            self.contraseña_temp = generate_password_hash(temp_password)
            # Configura la contraseña principal también
            self.set_password(temp_password)

    def check_password(self, password):
        """Verifica la contraseña principal."""
        return check_password_hash(self.contraseña, password)
