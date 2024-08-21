//js/dashboard.js

// Función para convertir la fecha en formato ISO
function convertirFecha(fecha) {
    return fecha.replace(' ', 'T') + 'Z'; 
}

// Función para calcular el tiempo transcurrido
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
        const estado = row.getAttribute('data-estado'); // Obtener el estado del tiquete
        const fechaAsignacion = row.getAttribute('data-fecha-asignacion');
        const tiempoTranscurridoElement = row.querySelector('.tiempo_transcurrido');
        
        if (estado === 'Finalizado' || estado === 'Cancelado') {
            tiempoTranscurridoElement.textContent = '00:00:00';
        } else {
            const tiempoTranscurrido = calcularTiempoTranscurrido(fechaAsignacion);
            tiempoTranscurridoElement.textContent = tiempoTranscurrido;
        }
    });
}

// Función para actualizar el color de fondo basado en el tiempo transcurrido
function actualizarColorSLA() {
    document.querySelectorAll('.tiquete').forEach(row => {
        const fechaAsignacion = row.getAttribute('data-fecha-asignacion');
        const minutosTotales = calcularTiempoTranscurridoEnMinutos(fechaAsignacion);

        const onTime = parseInt(row.getAttribute('data-on-time'));
        const runningLate = parseInt(row.getAttribute('data-running-late'));

        // Seleccionar el elemento con id "paint-status" dentro del card-header
        const statusElement = row.querySelector('#paint-status');

        if (statusElement) {
            // Comparar el tiempo transcurrido con los SLA y actualizar el color
            if (minutosTotales <= onTime) {
                statusElement.classList.add('sla-verde'); // Verde
                statusElement.classList.remove('sla-amarillo', 'sla-rojo');
            } else if (minutosTotales > onTime && minutosTotales <= runningLate) {
                statusElement.classList.add('sla-amarillo'); // Amarillo
                statusElement.classList.remove('sla-verde', 'sla-rojo');
            } else if (minutosTotales > runningLate) {
                statusElement.classList.add('sla-rojo'); // Rojo
                statusElement.classList.remove('sla-verde', 'sla-amarillo');
            }
        }
    });
}

// Función para convertir el tiempo transcurrido a minutos
function calcularTiempoTranscurridoEnMinutos(fechaAsignacion) {
    const ahora = new Date();
    const fechaISO = convertirFecha(fechaAsignacion);
    const fecha = new Date(fechaISO);

    if (isNaN(fecha.getTime())) {
        return 0; // Retornar 0 en caso de fecha inválida
    }

    const diferencia = ahora - fecha; // Diferencia en milisegundos
    const minutosTotales = Math.floor(diferencia / 60000); // Total en minutos

    return minutosTotales;
}

// Actualizar tiempo transcurrido y colores cada 1 segundo
function actualizarTodo() {
    actualizarTiempoTranscurrido();
    actualizarColorSLA();
}

// Actualizar cada x milisegundos
setInterval(actualizarTodo, 1000);

// Actualizar inmediatamente cuando se carga la página
document.addEventListener('DOMContentLoaded', actualizarTodo);
