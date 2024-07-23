'use strict';

function handleLoginResponse(response) {
    if (response.redirect_url) {
        // Si hay una URL de redirección, se redirige al usuario
        window.location.href = response.redirect_url;
    }

    if (response.alert_type && response.alert_message) {
        // Si hay un mensaje de alerta, se muestra
        Swal.fire({
            icon: response.alert_type,
            title: response.alert_type.charAt(0).toUpperCase() + response.alert_type.slice(1),
            text: response.alert_message
        });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => handleLoginResponse(data))
            .catch(error => {
                console.error('Error en el login:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema con el inicio de sesión. Por favor, inténtelo de nuevo.'
                });
            });
        });
    }
});
