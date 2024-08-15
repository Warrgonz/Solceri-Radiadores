from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from models.catalogo import Catalogo
from utils.firebase import FirebaseUtils
from utils.db import db
from models.cotizaciones import Cotizaciones
from models.mtl_cotizaciones import MtlCotizaciones
from models.tiquetes import Tiquetes
from datetime import datetime
from models.usuarios import Usuarios

cotizaciones_bp = Blueprint('cotizaciones', __name__)

@cotizaciones_bp.route('/cotizacion', methods=['GET', 'POST'])
def inicio():
    catalogo = Catalogo.query.all()
    cotizaciones = Cotizaciones.query.all()
    return render_template('cotizacion.html', catalogo=catalogo, cotizaciones=cotizaciones)

@cotizaciones_bp.route('/cotizacion/crear/<string:id_tiquete>', methods=['GET', 'POST'])
def crear_cotizacion(id_tiquete):
    print(f"ID del tiquete recibido: {id_tiquete}")
    
    if request.method == 'POST':
        try:
            user_id = session.get('user_id') 
            print(f"ID del usuario en sesión: {user_id}")
            
            fecha_creacion = datetime.utcnow()
            print(f"Fecha de creación: {fecha_creacion}")
    
            nueva_cotizacion = Cotizaciones(id_tiquete=id_tiquete, id_usuario=user_id, fecha_creacion=fecha_creacion)
            print(f"Cotización creada: {nueva_cotizacion}")
            
            db.session.add(nueva_cotizacion)
            db.session.commit()
            print(f"Cotización guardada en la base de datos con ID: {nueva_cotizacion.id_cotizacion}")

            # Responder con JSON si la cotización fue creada exitosamente
            return jsonify({
                'status': 'success',
                'message': 'Cotización creada exitosamente',
                'cotizacion_id': nueva_cotizacion.id_cotizacion
            }), 201
        
        except Exception as e:
            print(f"Error al crear la cotización: {str(e)}")
            db.session.rollback()
            # Responder con JSON en caso de error
            return jsonify({
                'status': 'error',
                'message': 'Hubo un error al crear la cotización',
                'error': str(e)
            }), 500
    
    # Si es un GET request, devolver la página de creación (opcional)
    usuarios = Usuarios.query.all()
    tiquete = Tiquetes.query.get_or_404(id_tiquete)
    print(f"Usuarios y tiquete cargados para el tiquete ID: {id_tiquete}")

    return render_template('crear_cotizacion.html', usuarios=usuarios, tiquete=tiquete)

@cotizaciones_bp.route('/cotizacion/editar/<int:id_cotizacion>', methods=['GET', 'POST'])
def cotizacion_editar(id_cotizacion):
    catalogo = Catalogo.query.all()
    cotizacion = Cotizaciones.query.get_or_404(id_cotizacion)


    return render_template('cotizacion_editar.html', cotizacion=cotizacion, catalogo=catalogo)

@cotizaciones_bp.route('/cotizacion/completar', methods=['POST'])
def completar_cotizacion():
    try:
        data = request.get_json()  # Asegúrate de recibir los datos en formato JSON
        id_cotizacion = data.get('id_cotizacion')
        productos = data.get('productos')

        if not productos:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron productos para la cotización.'
            }), 400
        
        # Iterar sobre los productos y agregar cada uno a la tabla MtlCotizaciones
        for producto in productos:
            id_catalogo = producto.get('id_catalogo')
            nombre_producto = producto.get('producto')
            cantidad = producto.get('cantidad')
            
            if id_catalogo is None:
                return jsonify({
                    'status': 'error',
                    'message': 'ID de catálogo no puede ser nulo.'
                }), 400
            
            nueva_mtl_cotizacion = MtlCotizaciones(
                id_catalogo=id_catalogo,
                producto=nombre_producto,
                cantidad=cantidad,
                id_cotizacion=id_cotizacion
            )
            
            db.session.add(nueva_mtl_cotizacion)
        
        # Guardar todos los cambios en la base de datos
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Productos añadidos a la cotización exitosamente'
        }), 201
        
    except Exception as e:
        print(f"Error al añadir productos a la cotización: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Hubo un error al añadir los productos a la cotización',
            'error': str(e)
        }), 500




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




