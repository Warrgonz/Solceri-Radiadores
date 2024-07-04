# routes/grupos.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.grupos import Grupos
from utils.db import db
from utils.auth import login_required, role_required

grupos_bp = Blueprint('grupos', __name__)

# Ruta para mostrar todos los equipos
@grupos_bp.route('/grupos')
@login_required
@role_required([1])
def grupos():
    grupos = Grupos.query.all()
    return render_template('grupos.html', grupos=grupos)

# Ruta para crear un nuevo equipo
@grupos_bp.route('/grupos/crear', methods=['GET', 'POST'])
def grupos_crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        nuevo_grupo = Grupos(nombre=nombre, descripcion=descripcion)
        db.session.add(nuevo_grupo)
        db.session.commit()

        return redirect(url_for('grupos.grupos'))  # Redirige a la lista de equipos

    return render_template('grupos_crear.html')

# Ruta para editar un equipo específico
@grupos_bp.route('/grupos/editar/<int:id_grupo>', methods=['GET', 'POST'])
def grupos_editar(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    if request.method == 'POST':
        if grupo:
            grupo.nombre = request.form['nombre']
            grupo.descripcion = request.form['descripcion']
            db.session.commit()
            return jsonify({'message': 'El grupo ha sido actualizado exitosamente'})
        else:
            return jsonify({'error': 'El grupo no existe'}), 404

    return render_template('grupos_editar.html', grupo=grupo)

# Ruta para eliminar un equipo específico
@grupos_bp.route('/grupos/eliminar/<int:id_grupo>', methods=['POST'])
def grupos_eliminar(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    if grupo:
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'message': 'El grupo ha sido eliminado exitosamente'})
    else:
        return jsonify({'error': 'El grupo no existe'}), 404