'use strict';

// Función para confirmar la eliminación
function confirmDelete(button) {
    const id_producto = button.getAttribute('data-id');
    const nombre_producto = button.getAttribute('data-producto');

    Swal.fire({
        title: `¿Estás seguro que deseas eliminar el producto "${nombre_producto}" del catálogo?`,
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: 'Eliminar',
        cancelButtonText: 'Cancelar',
        dangerMode: true,
    }).then((result) => {
        if (result.isConfirmed) {
            deleteProducto(id_producto);
        }
    });
}

// Función para enviar la solicitud DELETE al servidor
function deleteProducto(id) {
    fetch(`/catalogo/eliminar/${id}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al eliminar el producto');
        }
        return response.json();
    })
    .then(data => {
        Swal.fire(data.message, {
            icon: "success",
        }).then(() => {
            // Opcional: recargar la página o actualizar la lista de productos después de eliminar
            location.reload();
        });
    })
    .catch(error => {
        console.error('Error al eliminar el producto:', error);
        Swal.fire("Error al eliminar el producto", {
            icon: "error",
        });
    });
}

// Evento para filtrar la tabla por texto ingresado
document.addEventListener('DOMContentLoaded', function() {
    const inputBusqueda = document.getElementById('inputBusqueda');
    const tablaCatalogo = document.getElementById('tablaCatalogo').getElementsByTagName('tr');

    inputBusqueda.addEventListener('input', function() {
        const filtro = inputBusqueda.value.trim().toLowerCase();

        Array.from(tablaCatalogo).forEach(function(fila) {
            const textoFila = fila.textContent.trim().toLowerCase();
            const esVisible = textoFila.includes(filtro);
            fila.style.display = esVisible ? 'table-row' : 'none';
        });
    });
});
