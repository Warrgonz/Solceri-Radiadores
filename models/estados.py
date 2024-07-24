from utils.db import db

class Estados(db.Model):
    __tablename__ = 'estados'
    id_estado = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Estado(id_estado={self.id_estado}, estado='{self.estado}')>"