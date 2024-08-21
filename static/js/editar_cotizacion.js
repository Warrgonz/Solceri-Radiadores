// Esperamos que todos los elementos de la página carguen para ejecutar el script
document.addEventListener('DOMContentLoaded', function () {
    // Inicializamos el carrito y actualizamos badge y total
    inicializarCarrito();
    actualizarTotalCarrito();
    actualizarBadgeCarrito();
    
    // Asignamos eventos a los botones una vez que todo está listo
    ready();
});


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

function inicializarCarrito() {
    var carritoItems = document.getElementsByClassName('carrito-item');
    var totalItems = 0;
    var totalPrice = 0;

    // Recorrer todos los artículos en el carrito y sumar las cantidades y precios
    for (var i = 0; i < carritoItems.length; i++) {
        var item = carritoItems[i];
        var cantidadItem = parseInt(item.getElementsByClassName('carrito-item-cantidad')[0].value);
        var precioElemento = item.getElementsByClassName('carrito-item-precio')[0];
        var precio = parseFloat(precioElemento.innerText.replace('₡', '').replace(/\./g, '').replace(/,/g, '').trim());

        if (!isNaN(cantidadItem) && !isNaN(precio)) {
            totalItems += cantidadItem;
            totalPrice += cantidadItem * precio;
        }
    }

    // Actualizar el badge del carrito con el total de artículos
    document.getElementById('cart-badge').innerText = totalItems;

    // Actualizar el total del carrito con la suma de los precios
    document.getElementsByClassName('carrito-precio-total')[0].innerText = '₡' + totalPrice.toLocaleString('de-DE');
}

// Función que controla el botón clickeado de agregar al carrito
function agregarAlCarritoClicked(event) {
    var button = event.target;
    var item = button.closest('.card');  // Selecciona el contenedor de la tarjeta
    var titulo = item.getElementsByClassName('titulo-item')[0].innerText;
    var precioTexto = item.getElementsByClassName('precio-item')[0].innerText;

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

    // No pasar imagen al agregar al carrito
    agregarItemAlCarrito(titulo, precio);
    hacerVisibleCarrito();
}

// Función que agrega un item al carrito
function agregarItemAlCarrito(titulo, precio, idCatalogo = null) {
    var item = document.createElement('div');
    item.classList.add('carrito-item');
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
        <div class="carrito-item-detalles" ${idCatalogo ? `data-id-catalogo="${idCatalogo}"` : ''}>
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
    `;
    item.innerHTML = itemCarritoContenido;
    itemsCarrito.append(item);

    // Añadir funcionalidad eliminar, sumar y restar cantidad a los nuevos elementos
    item.getElementsByClassName('btn-eliminar')[0].addEventListener('click', eliminarItemCarrito);
    var botonRestarCantidad = item.getElementsByClassName('restar-cantidad')[0];
    botonRestarCantidad.addEventListener('click', restarCantidad);
    var botonSumarCantidad = item.getElementsByClassName('sumar-cantidad')[0];
    botonSumarCantidad.addEventListener('click', sumarCantidad);

    // Actualizar total y badge
    actualizarTotalCarrito();
    actualizarBadgeCarrito();
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
    actualizarBadgeCarrito();  

    ocultarCarrito();
}

function actualizarTotalCarrito() {
    var carritoContenedor = document.getElementsByClassName('carrito')[0];
    var carritoItems = carritoContenedor.getElementsByClassName('carrito-item');
    var total = 0;

    for (var i = 0; i < carritoItems.length; i++) {
        var item = carritoItems[i];
        var precioElemento = item.getElementsByClassName('carrito-item-precio')[0];
        var precio = parseFloat(precioElemento.innerText.replace('₡', '').replace(/\./g, '').replace(/,/g, '').trim());
        if (isNaN(precio)) {
            console.error("El precio no es un número válido:", precioElemento.innerText);
            precio = 0; 
        }
        var cantidadItem = parseInt(item.getElementsByClassName('carrito-item-cantidad')[0].value);
        total += precio * cantidadItem;
    }

    total = Math.round(total);

    document.getElementsByClassName('carrito-precio-total')[0].innerText = '₡' + total.toLocaleString('de-DE');
}

function actualizarBadgeCarrito() {
    var carritoItems = document.getElementsByClassName('carrito-item');
    var totalItems = 0;

    // Suma la cantidad de cada producto en el carrito
    for (var i = 0; i < carritoItems.length; i++) {
        var cantidad = parseInt(carritoItems[i].getElementsByClassName('carrito-item-cantidad')[0].value);
        totalItems += cantidad;
    }

    // Actualiza el badge con el total de artículos
    document.getElementById('cart-badge').innerText = totalItems;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('otroProductoLink').addEventListener('click', function(event) {
        event.preventDefault();
        toggleFormularioArticuloPersonalizado();
    });
});

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

    cancelarBtn.addEventListener('click', function(event) {
        event.preventDefault();
        form.style.display = 'none';
        link.style.display = 'block';
    });
}

document.querySelector('#crear-cotizacion button[type="submit"]').addEventListener('click', function(event) {
    event.preventDefault();
    agregarArticuloPersonalizado(event);
});

function agregarArticuloPersonalizado(event) {
    event.preventDefault();

    var form = document.getElementById('crear-cotizacion');
    var formData = new FormData(form);

    // Convertir el valor del precio a un entero para evitar el formato incorrecto
    var precio = parseInt(formData.get('precio').replace(/\./g, '').trim()); // Eliminar puntos y convertir a número entero
    formData.set('precio', precio); // Reemplazar el valor en formData con el número limpio

    fetch('/cotizacion/crear/otro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Añadir el artículo personalizado al carrito con el precio correcto
            agregarItemAlCarrito(data.nombre_producto, precio, data.ruta_imagen); // Aquí usamos el precio limpio

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

            // Actualizar el badge del carrito
            actualizarBadgeCarrito();
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

document.getElementById('completar-cotizacion-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var cartItems = [];
    var carritoItems = document.getElementsByClassName('carrito-item');

    for (var i = 0; i < carritoItems.length; i++) {
        var item = carritoItems[i];
        var titulo = item.getElementsByClassName('carrito-item-titulo')[0].innerText;
        var precio = parseInt(item.getElementsByClassName('carrito-item-precio')[0].innerText.replace('₡', '').replace(/\./g, '').replace(/,/g, '').trim());
        var cantidad = parseInt(item.getElementsByClassName('carrito-item-cantidad')[0].value);

        var productoData = {
            'producto': titulo,
            'precio': precio,
            'cantidad': cantidad
        };

        if (item.dataset.idCatalogo) {
            productoData['id_catalogo'] = item.dataset.idCatalogo;
        }

        cartItems.push(productoData);
    }

    document.getElementById('cart-items').value = JSON.stringify(cartItems);

    this.submit();
});
