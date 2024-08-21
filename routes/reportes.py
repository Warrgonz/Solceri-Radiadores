from utils.db import db
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for, json, send_file
from models.reportes import Reportes

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reportes', methods=['GET', 'POST'])
def inicio():
    colaboradores = db.session.query(Reportes.nombre_colaborador).distinct().all()
    clientes = db.session.query(Reportes.nombre_cliente).distinct().all()

    filtros = {
        'colaborador': '',
        'cliente': '',
        'fecha_inicio': '',
        'fecha_fin': '',
        'duracion_inicio': '',
        'duracion_fin': '',
        'id_tiquete': ''
    }
    resultados = None
    error_tiquete = None

    if request.method == 'POST':
        # Obtener los filtros seleccionados por el usuario
        filtros['colaborador'] = request.form.get('colaborador') or ''
        filtros['cliente'] = request.form.get('cliente') or ''
        filtros['fecha_inicio'] = request.form.get('fecha_inicio') or ''
        filtros['fecha_fin'] = request.form.get('fecha_fin') or ''
        filtros['duracion_inicio'] = request.form.get('duracion_inicio') or ''
        filtros['duracion_fin'] = request.form.get('duracion_fin') or ''
        filtros['id_tiquete'] = request.form.get('id_tiquete') or ''
        
        # Validar si el id_tiquete existe
        if filtros['id_tiquete']:
            tiquete_existe = db.session.query(Reportes.id_tiquete).filter_by(id_tiquete=filtros['id_tiquete']).first()
            if not tiquete_existe:
                error_tiquete = f"El ID de tiquete '{filtros['id_tiquete']}' no existe."
                return render_template('reportes.html', error_tiquete=error_tiquete, colaboradores=colaboradores, clientes=clientes, filtros=filtros)

        # Aplicar filtros y generar el reporte
        query = Reportes.query

        if filtros['colaborador']:
            query = query.filter(Reportes.nombre_colaborador.like(f"%{filtros['colaborador']}%"))
        if filtros['cliente']:
            query = query.filter(Reportes.nombre_cliente.like(f"%{filtros['cliente']}%"))
        if filtros['fecha_inicio']:
            query = query.filter(Reportes.fecha_cambio >= filtros['fecha_inicio'])
        if filtros['fecha_fin']:
            query = query.filter(Reportes.fecha_cambio <= filtros['fecha_fin'])
        if filtros['duracion_inicio']:
            query = query.filter(Reportes.tiempo_duracion >= int(filtros['duracion_inicio']) * 60)  # Convertir minutos a segundos
        if filtros['duracion_fin']:
            query = query.filter(Reportes.tiempo_duracion <= int(filtros['duracion_fin']) * 60)  # Convertir minutos a segundos
        if filtros['id_tiquete']:
            query = query.filter(Reportes.id_tiquete == filtros['id_tiquete'])

        resultados = query.all()

                # Imprimir los valores enviados por el formulario
        print("Datos enviados en el formulario:")
        print(f"Colaborador: {filtros['colaborador']}")
        print(f"Cliente: {filtros['cliente']}")
        print(f"Fecha de Inicio: {filtros['fecha_inicio']}")
        print(f"Fecha de Fin: {filtros['fecha_fin']}")
        print(f"Duración mínima: {filtros['duracion_inicio']}")
        print(f"Duración máxima: {filtros['duracion_fin']}")
        print(f"ID Tiquete: {filtros['id_tiquete']}")

    return render_template('reportes.html', 
                           resultados=resultados, 
                           filtros=filtros, 
                           colaboradores=colaboradores, 
                           clientes=clientes,
                           error_tiquete=error_tiquete)


@reportes_bp.route('/verificar_tiquete', methods=['POST'])
def verificar_tiquete():
    data = request.get_json()
    id_tiquete = data.get('id_tiquete', '')

    tiquete_existe = db.session.query(Reportes.id_tiquete).filter_by(id_tiquete=id_tiquete).first()

    if tiquete_existe:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False}), 404




