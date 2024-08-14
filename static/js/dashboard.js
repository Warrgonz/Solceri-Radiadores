function convertirFecha(fecha) {
    return fecha.replace(' ', 'T') + 'Z'; 
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
