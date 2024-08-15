from utils.db import db

class Estados(db.Model):
    __tablename__ = 'estados'
    id_estado = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Estado(id_estado={self.id_estado}, estado='{self.estado}')>"
    
    @staticmethod
    def set_estados():
        estados = [
            {"estado": "En progreso", "descripcion": "Tiquete en progreso"},
            {"estado": "En espera", "descripcion": "Tiquete en espera de respuesta o acción"},
            {"estado": "Llamar cliente", "descripcion": "Se debe contactar al cliente"},
            {"estado": "En camino", "descripcion": "Trabajador en camino para resolver el tiquete"},
            {"estado": "Entregado", "descripcion": "El servicio o producto ha sido entregado"},
            {"estado": "Finalizado", "descripcion": "Tiquete completado y cerrado"},
            {"estado": "Cancelado", "descripcion": "Tiquete cancelado"}
        ]
        
        for estado in estados:
            if not Estados.query.filter_by(estado=estado["estado"]).first():
                db.session.add(Estados(estado=estado["estado"], descripcion=estado["descripcion"]))
        
        db.session.commit()