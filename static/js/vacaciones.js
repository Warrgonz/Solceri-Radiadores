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


function setupSearchFilter() {
    const searchInput = document.getElementById('search-name');
    const table = document.getElementById('solicitudes-table');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    searchInput.addEventListener('input', function() {
        const searchValue = searchInput.value.toLowerCase();

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let match = false;

            for (let j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toLowerCase().includes(searchValue)) {
                    match = true;
                    break;
                }
            }

            rows[i].style.display = match ? '' : 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', setupSearchFilter);

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

// Estados de vacaciones

// Aceptar

function confirmarAceptacion(button) {
    const idSolicitud = button.getAttribute('data-id');
    const nombre = button.getAttribute('data-nombre');
    const primerApellido = button.getAttribute('data-primerapellido');
    const segundoApellido = button.getAttribute('data-segundoapellido');
    const diaInicio = button.getAttribute('data-diainicio');
    const diaFinal = button.getAttribute('data-diafinal');

    Swal.fire({
        title: '¿Desea aprobar las vacaciones?',
        text: `El solicitante ${nombre} ${primerApellido} ${segundoApellido} estará libre del ${diaInicio} al ${diaFinal}.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, aprobar',
        cancelButtonText: 'No, cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/vacaciones/aceptar_vacacion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id_solicitud: idSolicitud,
                    nombre: nombre,
                    primer_apellido: primerApellido,
                    segundo_apellido: segundoApellido,
                    dia_inicio: diaInicio,
                    dia_final: diaFinal
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Aprobado!',
                        'La solicitud de vacaciones ha sido aprobada.',
                        'success'
                    ).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire(
                        'Error',
                        'Hubo un problema al aprobar la solicitud.',
                        'error'
                    );
                }
            })
            .catch(error => {
                Swal.fire(
                    'Error',
                    `Hubo un problema al procesar la solicitud: ${error.message}`,
                    'error'
                );
            });
        }
    });
}

// Rechazar

function confirmarRechazo(button) {
    const idSolicitud = button.getAttribute('data-id');
    const nombre = button.getAttribute('data-nombre');
    const primerApellido = button.getAttribute('data-primerapellido');
    const segundoApellido = button.getAttribute('data-segundoapellido');
    const diaInicio = button.getAttribute('data-diainicio');
    const diaFinal = button.getAttribute('data-diafinal');

    Swal.fire({
        title: '¿Desea rechazar las vacaciones?',
        text: `El solicitante ${nombre} ${primerApellido} ${segundoApellido} solicita estar libre del ${diaInicio} al ${diaFinal}.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, rechazar',
        cancelButtonText: 'No, cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/vacaciones/rechazar_vacacion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id_solicitud: idSolicitud
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Rechazado!',
                        'La solicitud de vacaciones ha sido rechazada.',
                        'success'
                    ).then(() => {
                        location.reload(); // Recargar la página para reflejar los cambios
                    });
                } else {
                    Swal.fire(
                        'Error',
                        'Hubo un problema al rechazar la solicitud.',
                        'error'
                    );
                }
            });
        }
    });
}

// Cancelar aprobación

function cancelarAprobacion(button) {
    const idSolicitud = button.getAttribute('data-id');
    const nombre = button.getAttribute('data-nombre');
    const primerApellido = button.getAttribute('data-primerapellido');
    const segundoApellido = button.getAttribute('data-segundoapellido');

    Swal.fire({
        title: '¿Estás seguro que deseas cancelar estas vacaciones previamente aprobadas?',
        text: `Estás a punto de cancelar la aprobación de las vacaciones de ${nombre} ${primerApellido} ${segundoApellido}.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, dejar aprobado',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/vacaciones/cancelar_aprobacion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id_solicitud: idSolicitud
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Cancelado',
                        'La aprobación de las vacaciones ha sido cancelada.',
                        'success'
                    ).then(() => {
                        location.reload();  // Recargar la página para reflejar los cambios
                    });
                } else {
                    Swal.fire(
                        'Error',
                        'Hubo un problema al cancelar la aprobación.',
                        'error'
                    );
                }
            })
            .catch(error => {
                Swal.fire(
                    'Error',
                    'Hubo un problema al procesar la solicitud.',
                    'error'
                );
                console.error('Error:', error);
            });
        }
    });
}

// Cancelar solicitud

function cancelarSolicitud(idSolicitud) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Estás seguro que deseas cancelar esta solicitud de vacaciones? Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar!'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/vacaciones/cancelar_vacacion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id_solicitud: idSolicitud })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Cancelado!',
                        'La solicitud de vacaciones ha sido cancelada.',
                        'success'
                    ).then(() => {
                        location.reload();  // Recargar la página para reflejar los cambios
                    });
                } else {
                    Swal.fire(
                        'Error',
                        'No se pudo cancelar la solicitud.',
                        'error'
                    );
                }
            });
        }
    });
}

// Solicitud de cancelación

function solicitudCancelacionAprobacion(element) {
    const id = element.dataset.id;
    const nombre = element.dataset.nombre;
    const primerApellido = element.dataset.primerapellido;
    const segundoApellido = element.dataset.segundoapellido;
    const diaInicio = element.dataset.diainicio;
    const diaFinal = element.dataset.diafinal;

    Swal.fire({
        title: '¿Estás seguro?',
        text: `¿Estás seguro de solicitar la cancelación de las vacaciones de ${nombre} ${primerApellido} ${segundoApellido} del ${diaInicio} al ${diaFinal}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, solicitar cancelación',
        cancelButtonText: 'No, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/vacaciones/solicitud-cancelacion/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Solicitud Enviada',
                        'Tu solicitud de cancelación ha sido enviada a los administradores.',
                        'success'
                    );
                } else {
                    Swal.fire(
                        'Error',
                        data.message || 'No se pudo enviar la solicitud de cancelación.',
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error',
                    'Ha ocurrido un error al procesar tu solicitud.',
                    'error'
                );
            });
        }
    });
}



