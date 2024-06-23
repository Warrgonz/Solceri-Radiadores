from flask import Blueprint, render_template, request, jsonify
from models.usuarios import Usuarios

grupos_bp = Blueprint('grupos', __name__)

#Aqui todas las rutas para /grupos

@grupos_bp.route('/grupos')
def grupos():
    return render_template('grupos.html')

@grupos_bp.route('/grupos/create')
def grupos_create():
    return render_template('grupos_crear.html')

@grupos_bp.route('/grupos/editar')
def grupos_edit():
    return render_template('grupos_editar.html')

@grupos_bp.route('/grupos/buscar_usuarios', methods=['POST'])
def buscar_usuarios():
    query = request.form.get('query', '')
    usuarios = Usuarios.query.filter(Usuarios.nombre.like(f'%{query}%')).all()
    # Filtrar los usuarios cuyo rol sea Colaborador o Administrador
    usuarios = [usuario for usuario in usuarios if usuario.rol.nombre in ['Colaborador', 'Administrador']]
    resultados = [{'id_usuario': usuario.id_usuario, 'nombre': usuario.nombre} for usuario in usuarios]
    return jsonify(resultados)
