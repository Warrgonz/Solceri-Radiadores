from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from utils.db import db
from utils.auth import login_required, role_required
from models.usuarios import Usuarios
from models.grupos import Grupos
from models.categorias import Categorias
from models.tiquetes import Tiquetes
from models.tiquetes import Estados
from datetime import datetime


tiquetes_bp = Blueprint('tiquetes', __name__)

@tiquetes_bp.route('/tiquetes')
def tiquetes_listar():
    tiquetes = Tiquetes.query.all()
    return render_template('tiquetes.html', tiquetes=tiquetes)

@tiquetes_bp.route('/tiquete/crear', methods=['GET', 'POST'])
def tiquete_crear():
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        grupo_asignado = request.form.get('grupo_asignado')
        trabajador_designado = request.form.get('trabajador_designado')
        categoria = request.form.get('categoria')
        resumen = request.form.get('resumen')
        descripcion = request.form.get('descripcion')
        direccion = request.form.get('direccion')
        id_estado = request.form.get('estado')

        nuevo_tiquete = Tiquetes(
            id_cliente=id_cliente,
            grupo_asignado=grupo_asignado,
            trabajador_designado=trabajador_designado,
            categoria=categoria,
            resumen=resumen,
            descripcion=descripcion,
            direccion=direccion,
            id_estado=id_estado
        )

        try:
            db.session.add(nuevo_tiquete)
            db.session.commit()
            flash('Tiquete creado exitosamente', 'success')
            return redirect(url_for('tiquetes.tiquete_crear'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el tiquete: {str(e)}', 'danger')
            return redirect(url_for('tiquetes.tiquete_crear'))

    # Cargar datos necesarios para los selects
    clientes = Usuarios.query.filter_by(id_rol=3).all()  # Filtrar por rol de cliente
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()  # Admin y Colaboradores
    categorias = Categorias.query.all()
    estados = Estados.query.all()

    return render_template(
        'tiquete_crear.html',
        clientes=clientes,
        grupos=grupos,
        trabajadores=trabajadores,
        categorias=categorias,
        estados=estados,
        fecha_actual=datetime.utcnow()
    )




@tiquetes_bp.route('/tiquete/editar/<int:id_tiquete>', methods=['GET', 'POST'])
def tiquete_editar(id_tiquete):
    # Obtener el tiquete a editar
    tiquete = Tiquetes.query.get_or_404(id_tiquete)

    if request.method == 'POST':
        # Actualizar los campos con los datos del formulario
        tiquete.id_cliente = request.form.get('id_cliente')
        tiquete.grupo_asignado = request.form.get('grupo_asignado')
        tiquete.trabajador_designado = request.form.get('trabajador_designado')
        tiquete.categoria = request.form.get('categoria')
        tiquete.resumen = request.form.get('resumen')
        tiquete.descripcion = request.form.get('descripcion')
        tiquete.direccion = request.form.get('direccion')
        tiquete.id_estado = request.form.get('estado')

        try:
            db.session.commit()
            flash('Tiquete actualizado exitosamente', 'success')
            return redirect(url_for('tiquetes.tiquete_editar', id_tiquete=tiquete.id_tiquete))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el tiquete: {str(e)}', 'danger')
            return redirect(url_for('tiquetes.tiquete_editar', id_tiquete=tiquete.id_tiquete))

    # Cargar datos necesarios para los selects
    clientes = Usuarios.query.filter_by(id_rol=3).all()
    grupos = Grupos.query.all()
    trabajadores = Usuarios.query.filter(Usuarios.id_rol.in_([1, 2])).all()
    categorias = Categorias.query.all()
    estados = Estados.query.all()

    return render_template(
        'tiquete_editar.html',
        tiquete=tiquete,
        clientes=clientes,
        grupos=grupos,
        trabajadores=trabajadores,
        categorias=categorias,
        estados=estados,
        fecha_actual=datetime.utcnow()
    )
