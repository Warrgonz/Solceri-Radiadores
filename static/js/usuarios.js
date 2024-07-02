'use strict';

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