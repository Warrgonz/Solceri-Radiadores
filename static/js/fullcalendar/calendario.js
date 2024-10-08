'use strict';

let setLanguage = () => {
    return window.navigator.language === "es-ES" ? "es" : "en"
}

let btnRol = () => {
    let rol = document.getElementById("user_role").value;

    console.log(user_role)

    if (rol === "1") {
        return "solicitar"
    }
    return "solicitar"

}

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: setLanguage(), // Especifica el idioma aquí 
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: btnRol()
        },
        customButtons: {
            solicitar: {
                text: 'Solicitar',
                click: function () {
                    window.location.href = "/vacaciones/nueva";
                }
            },
            archivadas: {
                text: 'Archivadas',
                click: function () {
                    window.location.href = "/vacaciones/archivadas";
                }
            }
        },
        eventSources: {
            url: "/vacaciones/calendarizacion",
            failure: function(){
                alert("Hubo un error")
            }
        },       
        eventClick: function (info) {
            console.log(info.event.id)
            fetch('/vacaciones/info?id=' + info.event.id, {
                method: 'GET'
            }).then(response=>response.json()).then(data=>{
                document.getElementById('solicitanteVacacion').value = data.solicitante.nombre + " " + data.solicitante.primer_apellido + " " + data.solicitante.segundo_apellido
                document.getElementById('estadoVacacion').value = data.estado
                document.getElementById('aprobadorVacacion').value = data.aprobador.nombre + " " + data.aprobador.primer_apellido + " " + data.aprobador.segundo_apellido
                document.getElementById('inicioVacacion').value = data.dia_inicio
                document.getElementById('finalVacacion').value = data.dia_final
            })
            
            document.getElementById("btnDetalleVacacion").click()
        }
    });
    calendar.render();
});