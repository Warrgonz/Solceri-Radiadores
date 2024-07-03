'use strict';

// Alertas

document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500); // Remove the alert from the DOM after it fades out
        });
    }, 5000); // Time in milliseconds (4000ms = 4 seconds)
});

// Muestro el campo sobre la contratación

document.getElementById('rolSelect').addEventListener('change', function() {
    var selectedRole = this.options[this.selectedIndex].text;
    var fechaContratacionDiv = document.getElementById('fechaContratacionDiv');
    if (selectedRole === 'Administrador' || selectedRole === 'Colaborador') {
        fechaContratacionDiv.style.display = 'block';
    } else {
        fechaContratacionDiv.style.display = 'none';
    }
});

// Mostrar imagen seleccionada.

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var imgElement = document.getElementById('blah');
            imgElement.src = e.target.result;
            imgElement.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Buscar Usuarios

function buscarUsuarios() {
    var query = document.getElementById('buscar').value.toLowerCase();
    var usuarios = document.getElementsByClassName('usuario');

    for (var i = 0; i < usuarios.length; i++) {
        var usuario = usuarios[i];
        var cedula = usuario.getElementsByClassName('cedula')[0].textContent.toLowerCase();
        var nombreCompleto = usuario.getElementsByClassName('nombre-completo')[0].textContent.toLowerCase();
        var correo = usuario.getElementsByClassName('correo')[0].textContent.toLowerCase();

        if (cedula.includes(query) || nombreCompleto.includes(query) || correo.includes(query)) {
            usuario.style.display = '';
        } else {
            usuario.style.display = 'none';
        }
    }
}

// Desactivar usuarios.

function desactivarUsuario(cedula, id) {
    Swal.fire({
        title: '¿Está seguro?',
        text: `¿Está seguro que desea desactivar al usuario con cédula ${cedula}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, desactivar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Llamar a la ruta de Flask para desactivar el usuario
            fetch(`/usuarios/desactivar/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'  // Asegúrate de que csrf_token() esté definido correctamente en tu template
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Desactivado!',
                        'El usuario ha sido desactivado.',
                        'success'
                    ).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        'No se pudo desactivar el usuario.',
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'Ocurrió un error al intentar desactivar el usuario.',
                    'error'
                );
            });
        }
    });
}


// Activar usuario

function activarUsuario(cedula, id) {
    Swal.fire({
        title: '¿Está seguro?',
        text: `¿Está seguro que desea activar al usuario con cédula ${cedula}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, activar'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/usuarios/activar/${id}`, {  // Asegúrate de tener la ruta correcta para activar el usuario
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire(
                        'Activado!',
                        'El usuario ha sido activado.',
                        'success'
                    ).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        'No se pudo activar el usuario.',
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'Ocurrió un error al intentar activar el usuario.',
                    'error'
                );
            });
        }
    });
}

// Eliminar usuario

function confirmDelete(element) {
    const cedula = element.getAttribute('data-cedula');
    const deleteUrl = element.getAttribute('data-url');

    Swal.fire({
        title: '¿Está seguro?',
        text: `¿Está seguro que desea borrar el usuario con cédula ${cedula}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = deleteUrl;
        }
    });
}