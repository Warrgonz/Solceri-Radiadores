from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from models.categorias import Categorias
from utils.db import db

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias')
def categorias():
    categorias = Categorias.query.all() #Select * from categorias
    return render_template('categorias.html', categorias=categorias)

@categorias_bp.route('/categorias/nueva', methods=['GET', 'POST'])
def categorias_crear():
    if request.method == 'POST':
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        
        nueva_categoria = Categorias(categoria=categoria, descripcion=descripcion)
        
        # Guardar la nueva categoría en la base de datos
        db.session.add(nueva_categoria)
        db.session.commit()
        
        # Redirigir a la página de categorías después de guardar
        return redirect(url_for('categorias.categorias'))  # Redirige a la función categorias de este Blueprint
    
    # Si es GET, simplemente muestra el formulario para crear categorías
    return render_template('categorias_crear.html')


@categorias_bp.route('/categorias/editar/<int:id_categoria>', methods=['GET', 'POST'])
def editar_categoria(id_categoria):
    categoria = Categorias.query.get(id_categoria)
    if request.method == 'POST':
        if categoria:
            categoria.categoria = request.form['categoria']
            categoria.descripcion = request.form['descripcion']
            db.session.commit()
            return jsonify({'message': 'La categoría ha sido actualizada exitosamente'})
        else:
            return jsonify({'error': 'La categoría no existe'}), 404
    else:
        if categoria:
            return render_template('categorias_editar.html', categoria=categoria)
        else:
            return jsonify({'error': 'La categoría no existe'}), 404


@categorias_bp.route('/categorias/eliminar/<int:id_categoria>', methods=['POST'])
def categorias_eliminar(id_categoria):
    categoria = Categorias.query.get(id_categoria)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'message': 'La categoría ha sido eliminada exitosamente'})
    else:
        return jsonify({'error': 'La categoría no existe'}), 404

