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

    // Llama a la función cuando el documento esté listo
    document.addEventListener('DOMContentLoaded', VacacionSolicitada);

    // Establecer la fecha actual en el campo de fecha de inicio
    document.getElementById('dia_inicio').value = FechaFormularios(0); // Hoy

    // Establecer la fecha de mañana en el campo de fecha de finalización
    document.getElementById('dia_final').value = FechaFormularios(1); // Mañana