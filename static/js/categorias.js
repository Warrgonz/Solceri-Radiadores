'use strict';


// Editar categoria

document.addEventListener('DOMContentLoaded', function () {
    // Obtener el formulario de agregar categoría
    const agregarForm = document.getElementById('categoriaAgregarForm');
    if (agregarForm) {
        agregarForm.addEventListener('submit', function (event) {
            // Aquí puedes agregar cualquier lógica específica para agregar, si es necesario.
        });
    }

    // Obtener el formulario de editar categoría
    const editarForm = document.getElementById('categoriaEditarForm');
    if (editarForm) {
        editarForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Evita el envío del formulario

            Swal.fire({
                title: '¿Estás seguro?',
                text: "¿Quieres guardar los cambios?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, guardar cambios'
            }).then((result) => {
                if (result.isConfirmed) {
                    const formData = new FormData(editarForm);

                    fetch(editarForm.action, {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            Swal.fire(
                                '¡Guardado!',
                                data.message,
                                'success'
                            ).then(() => {
                                window.location.href = '/categorias';
                            });
                        } else {
                            Swal.fire(
                                'Error',
                                data.error,
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Error',
                            'Hubo un problema al intentar guardar los cambios.',
                            'error'
                        );
                    });
                }
            });
        });
    }
});

// Eliminar categoria

document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Evita el comportamiento por defecto del enlace
            
            const categoriaId = button.getAttribute('data-id');

            Swal.fire({
                title: '¿Estás seguro?',
                text: "No podrás revertir esto",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminarlo'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Enviar solicitud para eliminar la categoría
                    fetch(`/categorias/eliminar/${categoriaId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        } else {
                            throw new Error('Error al intentar eliminar la categoría');
                        }
                    })
                    .then(data => {
                        // Mostrar un SweetAlert de éxito
                        Swal.fire(
                            '¡Eliminado!',
                            'La categoría ha sido eliminada.',
                            'success'
                        ).then(() => {
                            location.reload(); // Recargar la página después de eliminar
                        });
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Error',
                            'Hubo un problema al intentar eliminar la categoría.',
                            'error'
                        );
                    });
                }
            });
        });
    });
});


