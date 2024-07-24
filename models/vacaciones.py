# models/usuarios.py

from utils.db import db

class Vacaciones(db.Model):
    __tablename__ = 'vacaciones'
    id_vacacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_solicitante = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_aprobador = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True) #
    estado = db.Column(db.String(255), nullable=False)
    detalles = db.Column(db.String(255), nullable=False)
    dia_inicio = db.Column(db.Date, nullable=False)
    dia_final = db.Column(db.Date, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=db.func.current_timestamp())
    dia_aprobacion = db.Column(db.DateTime, nullable=True) 

    solicitante = db.relationship('Usuarios', foreign_keys=[id_solicitante], backref='vacaciones_solicitadas')
    aprobador = db.relationship('Usuarios', foreign_keys=[id_aprobador], backref='vacaciones_aprobadas')