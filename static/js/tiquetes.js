//js/tiquetes.js

// Eliminar tiquete

function confirmDeleteTiquete(idTiquete) {
    Swal.fire({
        title: '¿Está seguro?',
        text: `¿Está seguro que desea eliminar el tiquete con ID ${idTiquete}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/tiquete/eliminar/${idTiquete}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'  // Asegúrate de que csrf_token() esté definido correctamente en tu template
                }
            })
            .then(response => {
                if (response.ok) {
                    Swal.fire(
                        'Eliminado!',
                        'El tiquete ha sido eliminado.',
                        'success'
                    ).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        'No se pudo eliminar el tiquete.',
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'Ocurrió un error al intentar eliminar el tiquete.',
                    'error'
                );
            });
        }
    });
}

function convertirFecha(fecha) {
    // Reemplaza el espacio entre la fecha y la hora por 'T' y añade una zona horaria opcional
    return fecha.replace(' ', 'T') + 'Z'; // Añade 'Z' para indicar UTC
}

function calcularTiempoTranscurrido(fechaAsignacion) {
    const ahora = new Date();
    const fechaISO = convertirFecha(fechaAsignacion);
    const fecha = new Date(fechaISO);

    if (isNaN(fecha.getTime())) {
        return 'Fecha inválida';
    }

    const diferencia = ahora - fecha; // Diferencia en milisegundos

    const segundosTotales = Math.floor(diferencia / 1000); // Total en segundos
    const horas = Math.floor(segundosTotales / 3600);
    const minutos = Math.floor((segundosTotales % 3600) / 60);
    const segundos = segundosTotales % 60;

    // Formatear en HH:MM:SS con ceros a la izquierda
    const formatoHoras = String(horas).padStart(2, '0');
    const formatoMinutos = String(minutos).padStart(2, '0');
    const formatoSegundos = String(segundos).padStart(2, '0');

    return `${formatoHoras}:${formatoMinutos}:${formatoSegundos}`;
}

function actualizarTiempoTranscurrido() {
    document.querySelectorAll('.tiquete').forEach(row => {
        const fechaAsignacion = row.getAttribute('data-fecha-asignacion');
        const tiempoTranscurrido = calcularTiempoTranscurrido(fechaAsignacion);
        row.querySelector('.tiempo_transcurrido').textContent = tiempoTranscurrido;
    });
}

// Actualizar cada x milisegundos
setInterval(actualizarTiempoTranscurrido, 1000);

// Actualizar inmediatamente cuando se carga la página
document.addEventListener('DOMContentLoaded', actualizarTiempoTranscurrido);