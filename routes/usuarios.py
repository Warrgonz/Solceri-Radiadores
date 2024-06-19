from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from models.usuarios import Usuarios

usuarios_bp = Blueprint('usuarios', __name__)

#Aqui todas las rutas para /usuarios

@usuarios_bp.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')