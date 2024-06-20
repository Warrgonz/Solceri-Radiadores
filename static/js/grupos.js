'use strict';

// Metodo que busca 
document.getElementById('busqueda').addEventListener('input', function() {
    let query = this.value;
    fetch('/grupos/buscar_usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${query}`
    })
    .then(response => response.json())
    .then(data => {
        let resultadosDiv = document.getElementById('resultados');
        resultadosDiv.innerHTML = '';
        data.forEach(resultado => {
            let p = document.createElement('p');
            p.textContent = resultado.nombre;
            p.setAttribute('data-id', resultado.id_usuario);
            p.addEventListener('click', function() {
                // Aquí puedes hacer algo con el ID del usuario seleccionado
            });
            resultadosDiv.appendChild(p);
        });
    });
});