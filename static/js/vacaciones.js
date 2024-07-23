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
    
    document.addEventListener('DOMContentLoaded', function() {
        // Obtener el valor actual de 'entries' desde los parámetros de la URL
        const urlParams = new URLSearchParams(window.location.search);
        const entries = urlParams.get('entries');
    
        // Si hay un valor de 'entries' en los parámetros, seleccionarlo en el <select>
        if (entries) {
            const entriesSelect = document.getElementById('entries');
            if (entriesSelect) {
                entriesSelect.value = entries;
            }
        }
    });


    // Llama a la función cuando el documento esté listo
    document.addEventListener('DOMContentLoaded', VacacionSolicitada);

    // Establecer la fecha actual en el campo de fecha de inicio
    document.getElementById('inicio_dia').value = FechaFormularios(0); // Hoy

    // Establecer la fecha de mañana en el campo de fecha de finalización
    document.getElementById('final_dia').value = FechaFormularios(1); // Mañana