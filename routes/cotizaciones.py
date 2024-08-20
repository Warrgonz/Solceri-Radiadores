from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for, json, send_file
from models.catalogo import Catalogo
from utils.firebase import FirebaseUtils
from utils.db import db
from models.cotizaciones import Cotizaciones
from models.mtl_cotizaciones import MtlCotizaciones
from models.tiquetes import Tiquetes
from datetime import datetime
from models.usuarios import Usuarios
from utils.servicio_mail import send_email_async
from models.facturas import Factura
from io import BytesIO
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


cotizaciones_bp = Blueprint('cotizaciones', __name__)

@cotizaciones_bp.route('/cotizacion', methods=['GET', 'POST'])
def inicio():
    catalogo = Catalogo.query.all()
    cotizaciones = Cotizaciones.query.all()

    cotizaciones_con_totales = []

    for cotizacion in cotizaciones:
        total = db.session.query(db.func.sum(MtlCotizaciones.precio)).filter_by(id_cotizacion=cotizacion.id_cotizacion).scalar()
        cotizaciones_con_totales.append({
            'cotizacion': cotizacion,
            'total': total if total else 0
        })

    return render_template('cotizacion.html', catalogo=catalogo, cotizaciones=cotizaciones_con_totales)

@cotizaciones_bp.route('/cotizacion/crear/<string:id_tiquete>', methods=['GET', 'POST'])
def crear_cotizacion(id_tiquete):   
    if request.method == 'POST':
        try:
            user_id = session.get('user_id') 

            fecha_creacion = datetime.utcnow()
    
            nueva_cotizacion = Cotizaciones(id_tiquete=id_tiquete, id_usuario=user_id, fecha_creacion=fecha_creacion)
            
            db.session.add(nueva_cotizacion)
            db.session.commit()

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

    user_id = session.get('user_id')

    user = Usuarios.query.get(user_id)
    
    return render_template('cotizacion_editar.html', cotizacion=cotizacion, catalogo=catalogo , user_role=user.rol.id_rol)

# Esto sirve para insertar el articulo "Custom" de la cotizacion.
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

@cotizaciones_bp.route('/cotizacion/completar', methods=['POST'])
def completar_cotizacion():
    try:
        id_cotizacion = request.form.get('id_cotizacion')
        cart_items = request.form.get('cart_items')
        
        if not cart_items:
            flash('No se recibieron productos en la solicitud.', 'error')
            return redirect(url_for('cotizaciones.inicio'))

        # Convertir el string JSON a una lista de diccionarios
        productos = json.loads(cart_items)

        if not productos:
            flash('No se proporcionaron productos para la cotización.', 'error')
            return redirect(url_for('cotizaciones.inicio'))

        # Iterar sobre los productos y agregar cada uno a la tabla MtlCotizaciones
        for producto in productos:
            nombre_producto = producto.get('producto')
            precio = producto.get('precio')
            cantidad = producto.get('cantidad')  # Asegúrate de obtener la cantidad

            nueva_mtl_cotizacion = MtlCotizaciones(
                producto=nombre_producto,
                precio=precio,
                cantidad=cantidad,  # Pasa 'cantidad' como argumento
                id_cotizacion=id_cotizacion
            )
            
            db.session.add(nueva_mtl_cotizacion)
        
        # Guardar todos los cambios en la base de datos
        db.session.commit()

        flash('Productos añadidos a la cotización exitosamente', 'success')
        return redirect(url_for('cotizaciones.inicio'))
        
    except Exception as e:
        print(f"Error al añadir productos a la cotización: {str(e)}")
        db.session.rollback()
        flash('Hubo un error al añadir los productos a la cotización.', 'error')
        return redirect(url_for('cotizaciones.inicio'))

    
@cotizaciones_bp.route('/cotizacion/enviar/<int:id_cotizacion>', methods=['POST'])
def enviar_cotizacion(id_cotizacion):
    try:
        cotizacion = Cotizaciones.query.get_or_404(id_cotizacion)
        items = cotizacion.items

        nombre_cliente = f"{cotizacion.tiquete.cliente.nombre} {cotizacion.tiquete.cliente.primer_apellido} {cotizacion.tiquete.cliente.segundo_apellido}"
        correo_cliente = cotizacion.tiquete.cliente.correo
        fecha_creacion = cotizacion.fecha_creacion.strftime("%d/%m/%Y")
        id_tiquete = cotizacion.tiquete.id_tiquete

        productos = []
        total = 0
        for i, item in enumerate(items, start=1):
            costo_total = item.precio * int(item.cantidad)
            total += costo_total
            productos.append({
                'no': i,
                'producto': item.producto,
                'precio': item.precio,
                'cantidad': item.cantidad,
                'costo_total': costo_total
            })
        
        count_cotizaciones = Factura.query.filter_by(id_tiquete=id_tiquete).count()
        numero_cotizacion = count_cotizaciones + 1  
        
        nombre_archivo = f"id_cotizacion_{id_cotizacion}_cotizacion_{numero_cotizacion}.html"

        html_content = render_template(
            'factura.html',
            nombre_cliente=nombre_cliente,
            correo_cliente=correo_cliente,
            fecha_creacion=fecha_creacion,
            id_tiquete=id_tiquete,
            productos=productos,
            total=total
        )

        # Escribir el contenido HTML en un BytesIO directamente
        file_bytes = BytesIO()
        file_bytes.write(html_content.encode('utf-8'))
        file_bytes.seek(0)  # Asegúrate de posicionar el puntero al inicio del archivo

        # Subir el archivo HTML a Firebase
        firebase_url = FirebaseUtils.post_cotizacion(file_bytes, filename=nombre_archivo)
        
        if not firebase_url:
            raise Exception("Error al subir la cotización a Firebase.")

        factura = Factura(
            id_tiquete=cotizacion.id_tiquete,
            id_usuario=cotizacion.id_usuario,
            cantidad_productos=len(items),
            archivo=firebase_url
        )
        db.session.add(factura)
        db.session.commit()

        subject = f"Factura de Cotización #{cotizacion.id_cotizacion}"
        body = f"""
        <html>
        <head></head>
        <body>
            <p>Estimado {nombre_cliente},</p>
            <p>Adjunto encontrarás la factura correspondiente a la cotización #{cotizacion.id_cotizacion}.</p>
            <p>Puedes acceder a la cotización haciendo clic en el siguiente enlace:</p>
            <p><a href="{firebase_url}" target="_blank">Ver Cotización</a></p>
            <p>También puedes visitar nuestro sitio web para más información:</p>
            <p><a href="https://solceri.com" style="background-color:#0087C3;color:white;padding:10px 20px;text-align:center;text-decoration:none;display:inline-block;border-radius:5px;" target="_blank">Visitar Solceri</a></p>
            <p>Gracias por confiar en nuestros servicios.</p>
            <p>Atentamente,<br>Solceri Radiadores</p>
        </body>
        </html>
        """
        send_email_async(correo_cliente, subject, body)

        flash('La cotización ha sido enviada exitosamente al cliente.', 'success')
        return jsonify({'status': 'success', 'message': 'La cotización ha sido enviada exitosamente al cliente.'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al enviar la cotización: {str(e)}")
        flash('Hubo un error al enviar la cotización.', 'danger')
        return jsonify({'status': 'error', 'message': 'Hubo un error al enviar la cotización.'})


@cotizaciones_bp.route('/cotizacion/eliminar/<int:id_cotizacion>', methods=['POST'])
def eliminar_cotizacion(id_cotizacion):
    try:
        cotizacion = Cotizaciones.query.get_or_404(id_cotizacion)
        
        # Eliminar todos los items asociados a la cotización
        MtlCotizaciones.query.filter_by(id_cotizacion=id_cotizacion).delete()

        # Eliminar la cotización
        db.session.delete(cotizacion)
        db.session.commit()

        flash('Cotización eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la cotización: {str(e)}', 'danger')

    return redirect(url_for('cotizaciones.inicio'))





