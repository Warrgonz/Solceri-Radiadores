from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.catalogo import Catalogo
from utils.db import db
from utils.firebase import FirebaseUtils
from utils.auth import login_required, role_required

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/catalogo')
@login_required
@role_required([1])
def catalogo():
    catalogo = Catalogo.query.all()  # Select * from catalogo
    print(catalogo)  # Imprime el contenido de catalogo en la consola de Flask
    return render_template('catalogo.html', catalogo=catalogo)

@catalogo_bp.route('/catalogo/create', methods=['GET', 'POST'])
def catalogo_crear():
    if request.method == 'POST':
        try:
            sku = request.form['sku']
            nombre_producto = request.form['producto']
            descripcion = request.form['descripcion']
            precio = request.form['precio'].strip()  # Obtener precio y eliminar espacios en blanco

            if not precio:  # Si precio está vacío después de eliminar espacios en blanco
                precio = None  # Establecer precio a None
                
            # Verificar si el SKU ya existe
            if Catalogo.query.filter_by(sku=sku).first():
                flash('El SKU ya existe. Por favor, elija otro.', 'danger')
                return redirect(url_for('catalogo.catalogo_crear'))

            # Verificar que los campos no estén vacíos
            if not sku or not nombre_producto or not descripcion:
                flash('Por favor, complete todos los campos obligatorios.', 'danger')
                return redirect(url_for('catalogo.catalogo_crear'))

            ruta_imagen = None

            if 'ruta_imagen' in request.files and request.files['ruta_imagen'].filename != '':
                file = request.files['ruta_imagen']
                ruta_imagen = FirebaseUtils.post_image(file)
            else:
                ruta_imagen = 'https://firebasestorage.googleapis.com/v0/b/solceri-1650a.appspot.com/o/system.png?alt=media&token=c6dd24e5-c288-4223-bbf9-152e4c007b51'

            nuevo_producto = Catalogo(
                sku=sku,
                nombre_producto=nombre_producto,
                descripcion=descripcion,
                precio=precio,
                ruta_imagen=ruta_imagen
            )

            db.session.add(nuevo_producto)
            db.session.commit()

            flash('Producto agregado exitosamente al catálogo', 'success')
            return redirect(url_for('catalogo.catalogo'))

        except Exception as e:
            print(f"Error al crear producto: {str(e)}")
            db.session.rollback()
            flash('Hubo un error al agregar el producto. Por favor, intente de nuevo.', 'danger')

    return render_template('catalogo_crear.html')

@catalogo_bp.route('/catalogo/edit/<int:id>', methods=['GET', 'POST'])
def catalogo_editar(id):
    producto = Catalogo.query.get_or_404(id)

    if request.method == 'POST':
        try:
            sku = request.form['sku']
            nombre_producto = request.form['producto']
            descripcion = request.form['descripcion']
            precio = request.form.get('precio', 0)

            # Actualizar la imagen si se proporciona un nuevo archivo
            nueva_imagen = None
            if 'ruta_imagen' in request.files and request.files['ruta_imagen'].filename != '':
                file = request.files['ruta_imagen']
                nueva_imagen = FirebaseUtils.update_image(file, producto.ruta_imagen)
            else:
                # Si no se proporciona un nuevo archivo, mantener la imagen actual
                nueva_imagen = producto.ruta_imagen

            # Actualizar los datos del producto
            producto.sku = sku
            producto.nombre_producto = nombre_producto
            producto.descripcion = descripcion
            producto.precio = precio
            producto.ruta_imagen = nueva_imagen

            db.session.commit()

            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('catalogo.catalogo'))

        except Exception as e:
            print(f"Error al actualizar el producto: {str(e)}")
            db.session.rollback()
            flash('Hubo un error al actualizar el producto. Por favor, intente de nuevo.', 'danger')

    return render_template('catalogo_editar.html', producto=producto)

@catalogo_bp.route('/catalogo/eliminar/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    try:
        # Obtener el producto a eliminar
        producto = Catalogo.query.get(id_producto)

        if not producto:
            return jsonify({'message': 'Producto no encontrado'}), 404

        # Eliminar la imagen de Firebase
        FirebaseUtils.delete_image(producto.ruta_imagen)

        # Eliminar el producto de la base de datos
        db.session.delete(producto)
        db.session.commit()

        return jsonify({'message': 'Producto eliminado correctamente'}), 200
    except Exception as e:
        print(f"Error al eliminar el producto: {str(e)}")
        return jsonify({'message': 'Error al eliminar el producto'}), 500


