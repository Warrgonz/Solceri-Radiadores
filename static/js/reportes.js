'use strict';

function validarFormulario(event) {
    // Prevenir el envío del formulario por defecto
    event.preventDefault();

    // Limpiar errores previos
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => input.classList.remove('report-error'));

    let formIsValid = true;

    const fechaInicio = document.getElementById('fecha_inicio');
    const fechaFin = document.getElementById('fecha_fin');
    const duracionInicio = document.getElementById('duracion_inicio');
    const duracionFin = document.getElementById('duracion_fin');
    const idTiquete = document.getElementById('id_tiquete');

    // Validar que la duración mínima no sea negativa
    if (duracionInicio.value && parseInt(duracionInicio.value) < 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error en la duración mínima',
            text: 'La duración mínima no puede ser negativa.',
        });
        duracionInicio.classList.add('report-error');
        formIsValid = false;
    }

    // Validar que la duración máxima no sea negativa
    if (duracionFin.value && parseInt(duracionFin.value) < 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error en la duración máxima',
            text: 'La duración máxima no puede ser negativa.',
        });
        duracionFin.classList.add('report-error');
        formIsValid = false;
    }

    // Validar que la duración mínima sea menor o igual a la máxima
    if (duracionInicio.value && duracionFin.value) {
        if (parseInt(duracionInicio.value) > parseInt(duracionFin.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Error en la duración',
                text: 'La duración mínima debe ser menor o igual a la duración máxima.',
            });
            duracionInicio.classList.add('report-error');
            duracionFin.classList.add('report-error');
            formIsValid = false;
        }
    }

    // Validar que la fecha de inicio sea menor o igual a la fecha de fin
    if (fechaInicio.value && fechaFin.value) {
        if (new Date(fechaInicio.value) > new Date(fechaFin.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Error en las fechas',
                text: 'La fecha de inicio debe ser menor o igual a la fecha de finalización.',
            });
            fechaInicio.classList.add('report-error');
            fechaFin.classList.add('report-error');
            formIsValid = false;
        }
    }

    // Verificar si el ID de tiquete existe
    if (idTiquete.value) {
        fetch('/verificar_tiquete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id_tiquete: idTiquete.value }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                if (formIsValid) {
                    document.getElementById('form-reporte').submit();  // Enviar el formulario si todo es válido
                }
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error en el ID de tiquete',
                    text: 'El ID de tiquete no existe.',
                });
                idTiquete.classList.add('report-error');
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Error en la verificación',
                text: 'Hubo un error al verificar el ID de tiquete.',
            });
        });
    } else {
        if (formIsValid) {
            document.getElementById('form-reporte').submit();  // Enviar el formulario si todo es válido
        }
    }
}

function limpiarFormulario() {
    document.getElementById('colaborador').selectedIndex = 0;
    document.getElementById('cliente').selectedIndex = 0;
    document.getElementById('fecha_inicio').value = '';
    document.getElementById('fecha_fin').value = '';
    document.getElementById('duracion_inicio').value = '';
    document.getElementById('duracion_fin').value = '';
    document.getElementById('id_tiquete').value = '';

    // Limpiar los bordes rojos
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => input.classList.remove('report-error'));
}
