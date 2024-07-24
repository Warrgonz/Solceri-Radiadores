# routes/grupos.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.grupos import Grupos
from utils.db import db
from utils.auth import login_required, role_required
from models.usuarios import Usuarios


grupos_bp = Blueprint('grupos', __name__)

# Ruta para mostrar todos los equipos
@grupos_bp.route('/grupos')
@login_required
@role_required([1])
def grupos():
    grupos = Grupos.query.all()
    return render_template('grupos.html', grupos=grupos)

@grupos_bp.route('/grupos/crear', methods=['GET', 'POST'])
def grupos_crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        usuarios_ids = request.form.getlist('usuarios')  # Obtén los IDs de los usuarios seleccionados

        nuevo_grupo = Grupos(nombre=nombre, descripcion=descripcion)
        db.session.add(nuevo_grupo)
        db.session.commit()

        for usuario_id in usuarios_ids:
            usuario = Usuarios.query.get(int(usuario_id))
            if usuario:
                nuevo_grupo.usuarios.append(usuario)

        db.session.commit()

        return redirect(url_for('grupos.grupos'))  # Redirige a la lista de grupos

    usuarios = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()
    return render_template('grupos_crear.html', usuarios=usuarios)


@grupos_bp.route('/grupos/editar/<int:id_grupo>', methods=['GET', 'POST'])
def grupos_editar(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    if request.method == 'POST':
        if grupo:
            grupo.nombre = request.form['nombre']
            grupo.descripcion = request.form['descripcion']
            db.session.commit()
            return jsonify({'message': 'Cambios guardados exitosamente'})
        else:
            return jsonify({'error': 'El grupo no existe'}), 404

    usuarios = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()
    return render_template('grupos_editar.html', grupo=grupo, usuarios=usuarios)

@grupos_bp.route('/grupos/agregar_usuario/<int:id_grupo>/<int:id_usuario>', methods=['POST'])
def agregar_usuario(id_grupo, id_usuario):
    grupo = Grupos.query.get(id_grupo)
    usuario = Usuarios.query.get(id_usuario)
    if grupo and usuario:
        if usuario not in grupo.usuarios:
            grupo.usuarios.append(usuario)
            db.session.commit()
            return jsonify({'message': 'Usuario agregado al grupo'})
        else:
            return jsonify({'error': 'El usuario ya está en el grupo'}), 400
    return jsonify({'error': 'Grupo o usuario no encontrado'}), 404


@grupos_bp.route('/grupos/remover_usuario/<int:id_grupo>/<int:id_usuario>', methods=['POST'])
def remover_usuario(id_grupo, id_usuario):
    grupo = Grupos.query.get(id_grupo)
    usuario = Usuarios.query.get(id_usuario)
    if grupo and usuario:
        grupo.usuarios.remove(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario removido del grupo'})
    return jsonify({'error': 'Grupo o usuario no encontrado'}), 404


@grupos_bp.route('/grupos/eliminar/<int:id_grupo>', methods=['POST'])
def grupos_eliminar(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    if grupo:
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo eliminado con éxito'}), 200
    else:
        return jsonify({'error': 'El grupo no existe'}), 404
    
@grupos_bp.route('/grupos/detalles/<int:id_grupo>')
@login_required
@role_required([1])
def grupos_detalles(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    if grupo:
        return render_template('grupos_detalles.html', grupo=grupo)
    return jsonify({'error': 'El grupo no existe'}), 404   