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