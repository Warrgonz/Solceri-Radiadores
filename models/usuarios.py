# models/usuarios.py

from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from itsdangerous import TimedSerializer as Serializer
from models.roles import Roles
from utils.servicio_mail import generate_temp_password, send_email_async
from flask import current_app
import jwt


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

    def generate_remember_token(self, expiration=2592000):  # 30 days
        payload = {
            'remember': self.id_usuario,
            'exp': datetime.utcnow() + timedelta(seconds=expiration)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_remember_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return Usuarios.query.get(payload['remember'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def create_admin_user():
    admin_email = "Warreno0419s@gmail.com"
    admin_cedula = "321654987"
    admin_nombre = "Solceri"
    admin_primer_apellido = "Forge"
    admin_segundo_apellido = "Radiadores"
    admin_estado = True
    admin_rol_id = 1
    admin_imagen_url = "https://firebasestorage.googleapis.com/v0/b/solceri-1650a.appspot.com/o/logoSolceri.png?alt=media&token=ae59e640-bba6-40f4-bce9-acb89c01d47f"

    # Verificar si los roles existen y crearlos si no existen
    roles = [
        {"rol": "Administrador", "descripcion": "Rol con privilegios administrativos"},
        {"rol": "Colaborador", "descripcion": "Rol para usuarios colaboradores"},
        {"rol": "Cliente", "descripcion": "Rol para usuarios clientes"}
    ]
    
    for role in roles:
        existing_role = Roles.query.filter_by(rol=role["rol"]).first()
        if not existing_role:
            new_role = Roles(rol=role["rol"], descripcion=role["descripcion"])
            db.session.add(new_role)
    
    db.session.commit()

    # Verificar si el usuario ya existe
    existing_user = Usuarios.query.filter_by(correo=admin_email).first()

    if not existing_user:
        # Generar una contraseña temporal
        temp_password = generate_temp_password()

        # Verificar si el rol de Administrador existe
        admin_role = Roles.query.filter_by(rol="Administrador").first()

        if not admin_role:
            print(f"No se encontró un rol de Administrador.")
            return

        # Crear el usuario administrador
        admin_user = Usuarios(
            cedula=admin_cedula,
            correo=admin_email,
            nombre=admin_nombre,
            primer_apellido=admin_primer_apellido,
            segundo_apellido=admin_segundo_apellido,
            id_rol=admin_role.id_rol,
            estado=admin_estado,
            ruta_imagen=admin_imagen_url  # Establecer la imagen predeterminada
        )

        # Guardar la contraseña temporal y la contraseña principal
        admin_user.contraseña_temp = generate_password_hash(temp_password)
        admin_user.set_password(temp_password)

        # Guardar el usuario en la base de datos
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario administrador creado exitosamente.")

        # Enviar correo electrónico con las credenciales
        subject = "Credenciales de Administrador"
        body = f"""
        <html>
        <head></head>
        <body>
            <h1>Bienvenido, {admin_nombre}</h1>
            <p>Tu cuenta de administrador ha sido creada con éxito.</p>
            <p><strong>Correo:</strong> {admin_email}</p>
            <p><strong>Contraseña:</strong> {temp_password}</p>
            <p>Por favor, inicia sesión y cambia tu contraseña lo antes posible.</p>
        </body>
        </html>
        """
        send_email_async(admin_email, subject, body)
    else:
        print("El usuario administrador ya existe.")



