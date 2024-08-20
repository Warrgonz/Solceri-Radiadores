// Esperamos que todos los elementos de la página carguen para ejecutar el script
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready();
}

function ready() {
    // Agregamos funcionalidad a los botones eliminar del carrito
    var botonesEliminarItem = document.getElementsByClassName('btn-eliminar');
    for (var i = 0; i < botonesEliminarItem.length; i++) {
        var button = botonesEliminarItem[i];
        button.addEventListener('click', eliminarItemCarrito);
    }

    // Agrego funcionalidad al botón sumar cantidad
    var botonesSumarCantidad = document.getElementsByClassName('sumar-cantidad');
    for (var i = 0; i < botonesSumarCantidad.length; i++) {
        var button = botonesSumarCantidad[i];
        button.addEventListener('click', sumarCantidad);
    }

    // Agrego funcionalidad al botón restar cantidad
    var botonesRestarCantidad = document.getElementsByClassName('restar-cantidad');
    for (var i = 0; i < botonesRestarCantidad.length; i++) {
        var button = botonesRestarCantidad[i];
        button.addEventListener('click', restarCantidad);
    }

    // Agregamos funcionalidad al botón Agregar al carrito
    var botonesAgregarAlCarrito = document.getElementsByClassName('boton-item');
    for (var i = 0; i < botonesAgregarAlCarrito.length; i++) {
        var button = botonesAgregarAlCarrito[i];
        button.addEventListener('click', agregarAlCarritoClicked);
    }

    // Agregamos funcionalidad al botón pagar
    document.getElementsByClassName('btn-pagar')[0].addEventListener('click', pagarClicked);
}

// Función que controla el botón clickeado de agregar al carrito
function agregarAlCarritoClicked(event) {
    var button = event.target;
    var item = button.closest('.card');  // Selecciona el contenedor de la tarjeta
    var titulo = item.getElementsByClassName('titulo-item')[0].innerText;
    var precioTexto = item.getElementsByClassName('precio-item')[0].innerText;
    var imagenSrc = item.getElementsByClassName('img-item')[0].src;

    // Extraer solo la parte numérica del texto de precio
    var precio = parseInt(precioTexto.replace('₡', '').replace('Precio:', '').replace(/,/g, '').trim());

    if (isNaN(precio)) {
        console.error("El precio no es un número válido:", precioTexto);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El precio del artículo no es válido.',
        });
        return;
    }

    agregarItemAlCarrito(titulo, precio, imagenSrc);
    hacerVisibleCarrito();
}

// Función que agrega un item al carrito
function agregarItemAlCarrito(titulo, precio, imagenSrc) {
    var item = document.createElement('div');
    item.classList.add('item');
    var itemsCarrito = document.getElementsByClassName('carrito-items')[0];

    // Controlamos que el item que intenta ingresar no se encuentre en el carrito
    var nombresItemsCarrito = itemsCarrito.getElementsByClassName('carrito-item-titulo');
    for (var i = 0; i < nombresItemsCarrito.length; i++) {
        if (nombresItemsCarrito[i].innerText === titulo) {
            Swal.fire({
                icon: 'warning',
                title: 'Artículo duplicado',
                text: 'El artículo ya se encuentra en el carrito',
            });
            return;
        }
    }

    var itemCarritoContenido = `
        <div class="carrito-item">
            <img src="${imagenSrc}" width="80px" alt="">
            <div class="carrito-item-detalles">
                <span class="carrito-item-titulo">${titulo}</span>
                <div class="selector-cantidad">
                    <i class="fa-solid fa-minus restar-cantidad"></i>
                    <input type="text" value="1" class="carrito-item-cantidad" disabled>
                    <i class="fa-solid fa-plus sumar-cantidad"></i>
                </div>
                <span class="carrito-item-precio">₡${precio.toLocaleString()}</span>
            </div>
            <button class="btn-eliminar">
                <i class="fa-solid fa-trash"></i>
            </button>
        </div>
    `;
    item.innerHTML = itemCarritoContenido;
    itemsCarrito.append(item);

    // Agregamos la funcionalidad eliminar al nuevo item
    item.getElementsByClassName('btn-eliminar')[0].addEventListener('click', eliminarItemCarrito);

    // Agregamos la funcionalidad restar cantidad del nuevo item
    var botonRestarCantidad = item.getElementsByClassName('restar-cantidad')[0];
    botonRestarCantidad.addEventListener('click', restarCantidad);

    // Agregamos la funcionalidad sumar cantidad del nuevo item
    var botonSumarCantidad = item.getElementsByClassName('sumar-cantidad')[0];
    botonSumarCantidad.addEventListener('click', sumarCantidad);

    // Actualizamos total
    actualizarTotalCarrito();
}

// Aumento en uno la cantidad del elemento seleccionado
function sumarCantidad(event) {
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    var cantidadActual = selector.getElementsByClassName('carrito-item-cantidad')[0].value;
    cantidadActual++;
    selector.getElementsByClassName('carrito-item-cantidad')[0].value = cantidadActual;
    actualizarTotalCarrito();
}

// Resto en uno la cantidad del elemento seleccionado
function restarCantidad(event) {
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    var cantidadActual = selector.getElementsByClassName('carrito-item-cantidad')[0].value;
    cantidadActual--;
    if (cantidadActual >= 1) {
        selector.getElementsByClassName('carrito-item-cantidad')[0].value = cantidadActual;
        actualizarTotalCarrito();
    }
}

// Elimino el item seleccionado del carrito
function eliminarItemCarrito(event) {
    var buttonClicked = event.target;
    buttonClicked.closest('.carrito-item').remove();  

    actualizarTotalCarrito();
    ocultarCarrito();
}

function actualizarTotalCarrito() {
    var carritoContenedor = document.getElementsByClassName('carrito')[0];
    var carritoItems = carritoContenedor.getElementsByClassName('carrito-item');
    var total = 0;

    for (var i = 0; i < carritoItems.length; i++) {
        var item = carritoItems[i];
        var precioElemento = item.getElementsByClassName('carrito-item-precio')[0];
        var precio = parseInt(precioElemento.innerText.replace('₡', '').replace(/,/g, '').trim());
        if (isNaN(precio)) {
            console.error("El precio no es un número válido:", precioElemento.innerText);
            precio = 0; 
        }
        var cantidadItem = parseInt(item.getElementsByClassName('carrito-item-cantidad')[0].value);
        total += precio * cantidadItem;
    }

    total = Math.round(total);

    document.getElementsByClassName('carrito-precio-total')[0].innerText = '₡' + total.toLocaleString();
}

function toggleFormularioArticuloPersonalizado() {
    var form = document.getElementById('crear-cotizacion');
    var link = document.getElementById('otroProductoLink');
    var cancelarBtn = document.querySelector('.btn-danger');

    if (form.style.display === 'block') {
        form.style.display = 'none';
        link.style.display = 'block';
    } else {
        form.style.display = 'block';
        link.style.display = 'none';
    }

    cancelarBtn.addEventListener('click', function (event) {
        form.style.display = 'none';  
        link.style.display = 'block'; 
    });
}

document.getElementById('otroProductoLink').addEventListener('click', function (event) {
    event.preventDefault(); 
    toggleFormularioArticuloPersonalizado();
});

function agregarArticuloPersonalizado(event) {
    event.preventDefault();

    var form = document.getElementById('crear-cotizacion');
    var formData = new FormData(form);

    fetch('/cotizacion/crear/otro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Añadir el artículo personalizado al carrito
            agregarItemAlCarrito(data.nombre_producto, parseInt(data.precio), data.ruta_imagen);

            // Mostrar notificación de éxito
            Swal.fire({
                icon: 'success',
                title: 'Artículo agregado',
                text: 'El artículo se ha agregado exitosamente a la cotización',
                showConfirmButton: false,
                timer: 2000
            });

            // Resetear el formulario y ocultarlo
            form.reset();  
            form.style.display = 'none';
            document.getElementById('otroProductoLink').style.display = 'block';
        } else if (data.status === 'error') {
            // Mostrar notificación de error si hubo un problema en la respuesta
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: data.message,
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Mostrar notificación de error si hubo un problema en la solicitud
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al agregar el artículo. Por favor, intente nuevamente.',
        });
    });
}

document.querySelector('#crear-cotizacion button[type="submit"]').addEventListener('click', agregarArticuloPersonalizado);

// Funcion para poder completar el detalle de la cotizacion
document.getElementById('completar-cotizacion-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var cartItems = [];
    var carritoItems = document.getElementsByClassName('carrito-item');

    for (var i = 0; i < carritoItems.length; i++) {
        var item = carritoItems[i];
        var titulo = item.getElementsByClassName('carrito-item-titulo')[0].innerText;
        var precio = parseInt(item.getElementsByClassName('carrito-item-precio')[0].innerText.replace('₡', '').replace(/,/g, '').trim());
        var cantidad = parseInt(item.getElementsByClassName('carrito-item-cantidad')[0].value);  // Captura la cantidad

        var productoData = {
            'producto': titulo,
            'precio': precio,
            'cantidad': cantidad  // Añade la cantidad al objeto
        };

        // Si es un artículo del catálogo, añade el ID del catálogo
        if (item.dataset.idCatalogo) {
            productoData['id_catalogo'] = item.dataset.idCatalogo;
        }

        cartItems.push(productoData);
    }

    document.getElementById('cart-items').value = JSON.stringify(cartItems);

    // Enviar el formulario
    this.submit();
});














