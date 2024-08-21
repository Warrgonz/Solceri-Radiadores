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
        nombre = request.form['nombre'].strip()
        descripcion = request.form['descripcion']

        # Captura los tiempos en minutos desde el formulario
        try:
            on_time = int(request.form['on_time'])
            running_late = int(request.form['running_late'])
            is_late = int(request.form['is_late'])
        except ValueError:
            return jsonify({'error': 'Los valores de tiempo deben ser números enteros válidos'}), 400

        # Validar la lógica de los tiempos
        if not (on_time < running_late < is_late):
            return jsonify({'error': 'Los tiempos de SLA deben cumplir con la lógica: On Time < Running Late < Is Late'}), 400

        # Validar que el nombre del grupo sea único
        nombre_existente = Grupos.query.filter(Grupos.nombre == nombre).first()
        if nombre_existente:
            return jsonify({'error': 'Ya existe un grupo con este nombre'}), 400

        # Crea el nuevo grupo con los SLA definidos
        nuevo_grupo = Grupos(nombre=nombre, descripcion=descripcion, on_time=on_time, running_late=running_late, is_late=is_late)
        db.session.add(nuevo_grupo)
        try:
            db.session.commit()
            return jsonify({'message': 'Grupo creado exitosamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return render_template('grupos_crear.html')


@grupos_bp.route('/grupos/editar/<int:id_grupo>', methods=['GET', 'POST'])
def grupos_editar(id_grupo):
    grupo = Grupos.query.get(id_grupo)
    if request.method == 'POST':
        if grupo:
            nuevo_nombre = request.form['nombre'].strip()
            nueva_descripcion = request.form['descripcion']

            # Captura los tiempos en minutos desde el formulario
            try:
                on_time = int(request.form['on_time'])
                running_late = int(request.form['running_late'])
                is_late = int(request.form['is_late'])
            except ValueError:
                return jsonify({'error': 'Los valores de tiempo deben ser números enteros válidos'}), 400

            # Validacion lógica de los tiempos
            if not (on_time < running_late < is_late):
                return jsonify({'error': 'Los tiempos de SLA deben cumplir con la lógica: On Time < Running Late < Is Late'}), 400

            # Validacion unicidad de nombre
            nombre_existente = Grupos.query.filter(Grupos.nombre == nuevo_nombre, Grupos.id_grupo != id_grupo).first()
            if nombre_existente:
                return jsonify({'error': 'Ya existe un grupo con este nombre'}), 400

            # Actualizar los valores del grupo
            grupo.nombre = nuevo_nombre
            grupo.descripcion = nueva_descripcion
            grupo.on_time = on_time
            grupo.running_late = running_late
            grupo.is_late = is_late

            try:
                db.session.commit()
                return jsonify({'message': 'Cambios guardados exitosamente'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
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