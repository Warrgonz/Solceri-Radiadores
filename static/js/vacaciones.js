'use strict';

// Función para obtener la fecha en formato YYYY-MM-DD
function FechaFormularios(days) {
    const today = new Date();
    today.setDate(today.getDate() + days);
    const yyyy = today.getFullYear();
    let mm = today.getMonth() + 1; // Los meses van de 0-11
    let dd = today.getDate();

    if (mm < 10) mm = '0' + mm;
    if (dd < 10) dd = '0' + dd;

    return `${yyyy}-${mm}-${dd}`;
}

function VacacionSolicitada() {
    // Verifica si hay un parámetro de alerta en la URL
    const urlParams = new URLSearchParams(window.location.search);
    const alert = urlParams.get('VacacionSolicitada_alert');

    if (alert === 'success') {
        Swal.fire({
            icon: 'success',
            title: '¡Solicitud enviada!',
            text: 'Tu solicitud ha sido enviada. El administrador revisará tu solicitud.',
            timer: 2000,
            showConfirmButton: false,  // Oculta el botón de confirmación
            timerProgressBar: true,   // Muestra la barra de progreso del temporizador
            confirmButtonText: 'Aceptar'
        });
    }
}

function updateEntries(value) {
    // Crear una URL con los parámetros de la página actual y la cantidad de entradas
    const url = new URL(window.location.href);
    url.searchParams.set('entries', value);

    // Redirigir a la nueva URL
    window.location.href = url.toString();
}

function VacacionModificada() {
    // Verifica si hay un parámetro de alerta en la URL
    const urlParams = new URLSearchParams(window.location.search);
    const alert = urlParams.get('VacacionModificada_alert');

    if (alert === 'success') {
        Swal.fire({
            icon: 'success',
            title: '¡Solicitud modificada!',
            text: 'Se ha modificado exitosamente la solicitud de vacaciones.',
            timer: 2000,
            showConfirmButton: false,  // Oculta el botón de confirmación
            timerProgressBar: true,   // Muestra la barra de progreso del temporizador
            confirmButtonText: 'Aceptar'
        });
    }
}

function cancelarSolicitud(solicitudId) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: 'POST',
                url: '/cancelar_solicitud',
                data: {
                    solicitud_id: solicitudId
                },
                success: function(response) {
                    if (response.success) {
                        Swal.fire(
                            'Cancelada!',
                            response.message,
                            'success'
                        ).then(() => {
                            // Refresca la página
                            location.reload();
                        });
                    } else {
                        Swal.fire(
                            'Error!',
                            response.message,
                            'error'
                        );
                    }
                },
                error: function() {
                    Swal.fire(
                        'Error!',
                        'No se pudo cancelar la solicitud.',
                        'error'
                    );
                }
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', VacacionModificada);

document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const entries = urlParams.get('entries');

    if (entries) {
        const entriesSelect = document.getElementById('entries');
        if (entriesSelect) {
            entriesSelect.value = entries;
        }
    }
});

document.addEventListener('DOMContentLoaded', VacacionSolicitada);

document.getElementById('inicio_dia').value = FechaFormularios(0); // Hoy

document.getElementById('final_dia').value = FechaFormularios(1); // Mañana