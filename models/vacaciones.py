# models/usuarios.py

from utils.db import db

# Un usuario (aprobador) puede aprobar varias solicitudes de vacaciones, y cada solicitud de vacaciones está asociada a un solicitante y un aprobador.

class Vacaciones(db.Model):
    __tablename__ = 'vacaciones'
    id_vacacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_aprobador = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    estado = db.Column(db.String(255), nullable=False)
    dia_inicio = db.Column(db.Date, nullable=False)
    dia_final = db.Column(db.Date, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=db.func.current_timestamp())
    dia_aprobacion = db.Column(db.DateTime, nullable=True)

    solicitante = db.relationship('Usuarios', foreign_keys=[id_usuario], backref=db.backref('solicitudes', lazy=True))
    aprobador = db.relationship('Usuarios', foreign_keys=[id_aprobador], backref=db.backref('aprobaciones', lazy=True))

    def __init__(self, id_usuario, estado, dia_inicio, dia_final, id_aprobador=None, dia_aprobacion=None):
        self.id_usuario = id_usuario
        self.estado = estado
        self.dia_inicio = dia_inicio
        self.dia_final = dia_final
        self.id_aprobador = id_aprobador
        self.dia_aprobacion = dia_aprobacion
        # self.fecha_solicitud = current_timestamp()
