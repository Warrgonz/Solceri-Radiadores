from utils.db import db

class Reportes(db.Model):
    __tablename__ = 'reportes'
    id_reportes = db.Column(db.Integer, primary_key=True, autoincrement=True)
