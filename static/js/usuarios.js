'use strict';

// Alerta de satisfaccion cuando se crea un usuario y se envia el correo

    // Escuchar el envío del formulario
    $('form').submit(function(event) {
        event.preventDefault();  // Evitar que se envíe el formulario normalmente

        // Realizar la petición AJAX
        $.ajax({
            type: 'POST',
            url: "{{ url_for('usuarios.usuarios_crear') }}",
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                // Mostrar Sweet Alert si la creación fue exitosa
                Swal.fire({
                    icon: 'success',
                    title: '¡Usuario creado exitosamente!',
                    text: 'Acceso a la aplicación generado.',
                    showConfirmButton: false,
                    timer: 3000  // Cerrar automáticamente después de 3 segundos
                }).then(function() {
                    window.location.href = "{{ url_for('usuarios.usuarios') }}";  // Redirigir al listado de usuarios
                });
            },
            error: function(error) {
                // Mostrar alerta de error si ocurrió algún problema
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.responseJSON.error  // Mostrar el mensaje de error del servidor
                });
            }
        });
    });