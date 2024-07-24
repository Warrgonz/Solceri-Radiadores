from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.grupos import Grupos
from utils.db import db
from utils.auth import login_required, role_required
from models.usuarios import Usuarios
from models.grupos import Grupos
from models.categorias import Categorias
from models.tiquetes import Tiquetes
from models.tiquetes import Estados

tiquetes_bp = Blueprint('tiquetes', __name__)

@tiquetes_bp.route('/tiquetes')
def tiquetes_listar():
    tiquetes = Tiquetes.query.all()
    return render_template('tiquetes.html', tiquetes=tiquetes)

@tiquetes_bp.route('/tiquete/crear', methods=['GET', 'POST'])
def tiquete_crear():
    if request.method == 'POST':
        resumen = request.form['resumen']
        descripcion = request.form['descripcion']
        id_cliente = request.form['id_cliente']
        grupo_asignado = request.form['grupo_asignado']
        trabajador_designado = request.form['trabajador_designado']
        categoria = request.form['categoria']
        estado = request.form['estado']
        
        tiquete = Tiquetes(
            resumen=resumen,
            descripcion=descripcion,
            id_cliente=id_cliente,
            grupo_asignado=grupo_asignado,
            trabajador_designado=trabajador_designado,
            categoria=categoria,
            estado=estado
        )
        db.session.add(tiquete)
        db.session.commit()
        
        return redirect(url_for('tiquetes.tiquetes_listar'))
    
    clientes = Usuarios.query.all()
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.all()  # Supongo que los trabajadores también están en Usuarios
    categorias = Categorias.query.all()
    estados = Estados.query.all()
    
    return render_template('tiquete_crear.html', clientes=clientes, grupos=grupos, trabajadores=trabajadores, categorias=categorias, estados=estados)

@tiquetes_bp.route('/tiquete/editar/<int:id_tiquete>', methods=['GET', 'POST'])
def tiquete_editar(id_tiquete):
    tiquete = Tiquetes.query.get_or_404(id_tiquete)
    
    if request.method == 'POST':
        tiquete.resumen = request.form['resumen']
        tiquete.descripcion = request.form['descripcion']
        tiquete.id_cliente = request.form['id_cliente']
        tiquete.grupo_asignado = request.form['grupo_asignado']
        tiquete.trabajador_designado = request.form['trabajador_designado']
        tiquete.categoria = request.form['categoria']
        tiquete.estado = request.form['estado']
        tiquete.ultima_asignacion = db.func.now()
        
        db.session.commit()
        return redirect(url_for('tiquetes.tiquetes_listar'))
    
    clientes = Usuarios.query.all()
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.all()  # Supongo que los trabajadores también están en Usuarios
    categorias = Categorias.query.all()
    estados = Estados.query.all()
    
    return render_template('tiquete_editar.html', tiquete=tiquete, clientes=clientes, grupos=grupos, trabajadores=trabajadores, categorias=categorias, estados=estados)

@tiquetes_bp.route('/tiquete/eliminar/<int:id_tiquete>', methods=['POST'])
def tiquete_eliminar(id_tiquete):
    tiquete = Tiquetes.query.get(id_tiquete)
    if tiquete:
        db.session.delete(tiquete)
        db.session.commit()
        return jsonify({'message': 'Tiquete eliminado exitosamente'})
    else:
        return jsonify({'error': 'El tiquete no existe'}), 404
