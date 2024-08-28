import pandas as pd
from io import BytesIO
from flask import Blueprint, render_template, request, send_file
from models.reportes import Reportes
from datetime import datetime

reportes_bp = Blueprint('reportes', __name__)

def convertir_a_hhmmss(segundos):
    """Convierte los segundos a formato hh:mm:ss."""
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    return f"{horas:02}:{minutos:02}:{segundos_restantes:02}"

@reportes_bp.route('/reportes', methods=['GET', 'POST'])
def mostrar_reportes():
    # Obtener filtros de la solicitud
    trabajador = request.args.get('trabajador', None)
    cliente = request.args.get('cliente', None)
    fecha_inicio = request.args.get('fecha_inicio', None)
    fecha_fin = request.args.get('fecha_fin', None)

    # Construir la consulta base
    reportes = Reportes.query

    # Aplicar filtro si se especifica un trabajador
    if trabajador:
        reportes = reportes.filter(Reportes.nombre_colaborador == trabajador)
    
    # Aplicar filtro si se especifica un cliente
    if cliente:
        reportes = reportes.filter(Reportes.nombre_cliente == cliente)

    # Aplicar filtro por rango de fechas
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        reportes = reportes.filter(Reportes.fecha_cambio >= fecha_inicio)
    
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        reportes = reportes.filter(Reportes.fecha_cambio <= fecha_fin)

    # Ejecutar la consulta
    reportes = reportes.all()

    # Convertir tiempo de duración a formato hh:mm:ss
    for reporte in reportes:
        reporte.tiempo_duracion_formateado = convertir_a_hhmmss(reporte.tiempo_duracion) if reporte.tiempo_duracion else 'N/A'

    # Obtener estadísticas
    total_tiquetes = len(reportes)
    tiempo_promedio = (
        convertir_a_hhmmss(
            round(sum([r.tiempo_duracion for r in reportes if r.tiempo_duracion is not None]) / len(reportes))
        ) if reportes else '00:00:00'
    )

    estadisticas = {
        'total_tiquetes': total_tiquetes,
        'tiempo_promedio': tiempo_promedio
    }

    # Obtener lista única de trabajadores y clientes para los filtros
    trabajadores = Reportes.query.with_entities(Reportes.nombre_colaborador).distinct().all()
    trabajadores = [t[0] for t in trabajadores]

    clientes = Reportes.query.with_entities(Reportes.nombre_cliente).distinct().all()
    clientes = [c[0] for c in clientes]

    # Renderizar la plantilla con los datos
    return render_template('reportes.html', reportes=reportes, estadisticas=estadisticas, trabajadores=trabajadores, clientes=clientes)

@reportes_bp.route('/exportar_reportes', methods=['GET'])
def exportar_reportes():
    # Obtener filtros de la solicitud
    trabajador = request.args.get('trabajador', None)
    cliente = request.args.get('cliente', None)
    fecha_inicio = request.args.get('fecha_inicio', None)
    fecha_fin = request.args.get('fecha_fin', None)

    # Construir la consulta base
    reportes = Reportes.query

    # Aplicar filtro si se especifica un trabajador
    if trabajador:
        reportes = reportes.filter(Reportes.nombre_colaborador == trabajador)
    
    # Aplicar filtro si se especifica un cliente
    if cliente:
        reportes = reportes.filter(Reportes.nombre_cliente == cliente)

    # Aplicar filtro por rango de fechas
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        reportes = reportes.filter(Reportes.fecha_cambio >= fecha_inicio)
    
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        reportes = reportes.filter(Reportes.fecha_cambio <= fecha_fin)

    # Ejecutar la consulta
    reportes = reportes.all()

    # Convertir tiempo de duración a formato hh:mm:ss
    for reporte in reportes:
        reporte.tiempo_duracion_formateado = convertir_a_hhmmss(reporte.tiempo_duracion) if reporte.tiempo_duracion else 'N/A'

    # Obtener estadísticas
    total_tiquetes = len(reportes)
    tiempo_promedio = (
        convertir_a_hhmmss(
            round(sum([r.tiempo_duracion for r in reportes if r.tiempo_duracion is not None]) / len(reportes))
        ) if reportes else '00:00:00'
    )

    # Crear un DataFrame con pandas
    df = pd.DataFrame([{
        "ID Reporte": reporte.id_reportes,
        "ID Tiquete": reporte.id_tiquete,
        "Colaborador": reporte.nombre_colaborador or 'N/A',
        "Cliente": reporte.nombre_cliente or 'N/A',
        "Fecha": reporte.fecha_cambio.strftime('%Y-%m-%d'),
        "Tiempo de Duración (hh:mm:ss)": reporte.tiempo_duracion_formateado
    } for reporte in reportes])

    # Crear un archivo Excel en memoria usando BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Reportes')

        # Crear DataFrame para las estadísticas y filtros
        stats_df = pd.DataFrame({
            "Metric": ["Total de Tiquetes", "Tiempo Promedio", "Trabajador", "Cliente", "Fecha de Inicio", "Fecha de Fin"],
            "Value": [
                total_tiquetes,
                tiempo_promedio,
                trabajador if trabajador else 'Todos',
                cliente if cliente else 'Todos',
                fecha_inicio.strftime('%Y-%m-%d') if fecha_inicio else 'Sin especificar',
                fecha_fin.strftime('%Y-%m-%d') if fecha_fin else 'Sin especificar'
            ]
        })
        stats_df.to_excel(writer, index=False, sheet_name='Estadísticas')

    # Mover el cursor al inicio del archivo
    output.seek(0)

    # Enviar el archivo Excel al usuario
    return send_file(output, as_attachment=True, download_name="reportes.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")