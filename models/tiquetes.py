#models/tiquetes.py

from utils.db import db
from models.usuarios import Usuarios  
from models.grupos import Grupos  
from models.categorias import Categorias

class Estados(db.Model):
    __tablename__ = 'estados'
    id_estado = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Estado(id_estado={self.id_estado}, estado='{self.estado}')>"

class Tiquetes(db.Model):
    __tablename__ = 'tiquetes'
    id_tiquete = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    grupo_asignado = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=True)
    trabajador_designado = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    ultima_asignacion = db.Column(db.DateTime, nullable=True)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)

    cliente = db.relationship('Usuarios', foreign_keys=[id_cliente])
    grupo = db.relationship('Grupos', foreign_keys=[grupo_asignado])
    trabajador = db.relationship('Usuarios', foreign_keys=[trabajador_designado])
    estado = db.relationship('Estados', foreign_keys=[id_estado])

    def __repr__(self):
        return f"<Tiquete(id_tiquete={self.id_tiquete}, resumen='{self.resumen}')>"

