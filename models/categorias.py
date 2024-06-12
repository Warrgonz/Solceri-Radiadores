from utils.db import db

class Categorias(db.Model):
    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))
    
    # Constructor
    def __init__(self, categoria, descripcion):
        self.categoria = categoria
        self.descripcion = descripcion

    