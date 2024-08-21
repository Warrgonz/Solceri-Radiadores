from utils.db import db

class Reportes(db.Model):
    __tablename__ = 'reportes'
    id_reportes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tiquete = db.Column(db.String(10), db.ForeignKey('tiquetes.id_tiquete', ondelete='CASCADE'), nullable=False)
    nombre_colaborador = db.Column(db.String(255), nullable=True)  
    nombre_cliente = db.Column(db.String(255), nullable=True)     
    fecha_cambio = db.Column(db.DateTime, nullable=False)
    tiempo_duracion = db.Column(db.Integer, nullable=True)

    def __init__(self, id_tiquete, nombre_colaborador=None, nombre_cliente=None, tiempo_duracion=None):
        self.id_tiquete = id_tiquete
        self.nombre_colaborador = nombre_colaborador
        self.nombre_cliente = nombre_cliente
        self.tiempo_duracion = tiempo_duracion

    def __repr__(self):
        return f'<Reporte #{self.id_reportes} para Tiquete #{self.id_tiquete}>'
