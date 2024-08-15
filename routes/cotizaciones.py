from flask import Blueprint, render_template, request, jsonify
from models.catalogo import Catalogo
from utils.firebase import FirebaseUtils
from utils.db import db
from models.cotizaciones import Cotizaciones
from models.mtl_cotizaciones import MtlCotizaciones

cotizaciones_bp = Blueprint('cotizaciones', __name__)

@cotizaciones_bp.route('/cotizacion', methods=['GET', 'POST'])
def inicio():
    catalogo = Catalogo.query.all()
    return render_template('cotizacion.html', catalogo=catalogo)

@cotizaciones_bp.route('/cotizacion/crear', methods=['GET', 'POST'])
def crear_cotizacion():
    catalogo = Catalogo.query.all()
    return render_template('cotizacion_crear.html', catalogo=catalogo)






@cotizaciones_bp.route('/cotizacion/crear/otro', methods=['GET', 'POST'])
def articulo_crear():
    try:
        nombre_producto = request.form['producto']
        descripcion = request.form['descripcion']
        precio = request.form['precio'].strip()

        try:
            precio = int(precio)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'El precio debe ser un número entero válido.'}), 400

        ruta_imagen = None
        if 'ruta_imagen' in request.files and request.files['ruta_imagen'].filename != '':
            file = request.files['ruta_imagen']
            ruta_imagen = FirebaseUtils.post_image(file)
        else:
            ruta_imagen = 'https://firebasestorage.googleapis.com/v0/b/solceri-1650a.appspot.com/o/logoSolceri.png?alt=media&token=ae59e640-bba6-40f4-bce9-acb89c01d47f'

        return jsonify({
            'status': 'success',
            'nombre_producto': nombre_producto,
            'descripcion': descripcion,
            'precio': precio,
            'ruta_imagen': ruta_imagen
        }), 200

    except Exception as e:
        print(f"Error al procesar artículo: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Hubo un error al procesar el artículo. Por favor, intente de nuevo.'}), 500




