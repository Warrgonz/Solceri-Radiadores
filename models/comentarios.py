# models/comentarios.py
from utils.db import db
from datetime import datetime

class Comentarios(db.Model):
    __tablename__ = 'comentarios'
    id_comentario = db.Column(db.Integer, primary_key=True)
    id_tiquete = db.Column(db.String(10), db.ForeignKey('tiquetes.id_tiquete'), nullable=False)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    visible_cliente = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relaciones
    tiquete = db.relationship('Tiquetes', back_populates='comentarios')