document.addEventListener('DOMContentLoaded', function() {

    let request_calendar = "./events.json"

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        events:function(info, successCallback, failureCallback){
            fetch(request_calendar)
                .then(function(response){
                    return response.json()
                })
                .then(function(data){
                    let events = data.events.map(function(event){
                        return {
                            title: event.eventTitle,
                            start: new Date(event.eventStartDate),
                            end: new Date(event.eventEndDate),
                            tipo: event.eventTipo,
                            timeStart: event.eventStartTime,
                            timeEnd: event.eventEndTime,
                        }
                    })
                    successCallback(events)
                })
                .catch(function(error){
                    failureCallback(error)
                })
        },

        eventContent: function(info){
            console.log("Hola Mundo!")
            return {
                html: `
                <div style="overflow: hidden; font-size: 12px; positon: relative;  cursor: pointer; font-family: 'Inter', sans-serif;">
                    <div><strong>${info.event.title}</strong></div>
                    <div>Tipo: ${info.event.extendedProps.tipo}</div>
                    <div>Date: ${info.event.start.toLocaleDateString(
                        "es-US",
                        {
                            month: "long",
                            day: "numeric",
                            year: "numeric",
                        }
                    )}</div>
                    <div>Time: ${info.event.extendedProps.timeStart} - ${info.event.extendedProps.timeEnd}</div>
                </div>
                `
            }
        },

  eventMouseEnter: function(mouseEnterInfo){
            console.log(mouseEnterInfo)
            let el = mouseEnterInfo.el
            el.classList.add("relative")

            let newEl = document.createElement("div")
            let newElTitle = mouseEnterInfo.event.title
            let newElTipo = mouseEnterInfo.event.tipo
            newEl.innerHTML = `
                <div
                    class="fc-hoverable-event"
                    style="position: absolute; bottom: 100%; left: 0; width: 300px; height: auto; background-color: white; z-index: 50; border: 1px solid #e2e8f0; border-radius: 0.375rem; padding: 0.75rem; font-size: 14px; font-family: 'Inter', sans-serif; cursor: pointer;"
                >
                    <strong>${newElTitle}</strong>
                    <div>Tipo: ${newElTipo}</div>

                </div>
            `
            el.after(newEl)
        },

        eventMouseLeave: function(){
            document.querySelector(".fc-hoverable-event").remove()
        }
    });
    calendar.render();
});