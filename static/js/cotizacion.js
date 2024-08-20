'use strict';

// Enviar cotización

function confirmarEnviarCotizacion(idCotizacion) {
    Swal.fire({
        title: '¿Deseas enviar esta cotización?',
        text: "Se enviará al cliente como un PDF adjunto.",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, enviar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/cotizacion/enviar/${idCotizacion}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'  // Si estás usando protección CSRF
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    Swal.fire(
                        'Enviado',
                        'La cotización ha sido enviada exitosamente.',
                        'success'
                    );
                } else {
                    Swal.fire(
                        'Error',
                        'Hubo un problema al enviar la cotización.',
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error al enviar la cotización:', error);
                Swal.fire(
                    'Error',
                    'Hubo un problema al enviar la cotización. Intente nuevamente más tarde.',
                    'error'
                );
            });
        }
    });
}

// Eliminar cotizacion

function confirmarEliminarCotizacion(idCotizacion) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡Esta acción no se puede deshacer!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Crear un formulario temporal para enviar la solicitud POST
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/cotizacion/eliminar/${idCotizacion}`;

            // Agregar un token CSRF si es necesario (depende de tu configuración)
            const csrfToken = document.querySelector('input[name="csrf_token"]');
            if (csrfToken) {
                const inputCsrf = document.createElement('input');
                inputCsrf.type = 'hidden';
                inputCsrf.name = 'csrf_token';
                inputCsrf.value = csrfToken.value;
                form.appendChild(inputCsrf);
            }

            document.body.appendChild(form);
            form.submit();
        }
    });
}
