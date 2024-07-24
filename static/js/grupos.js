'use strict';

document.addEventListener('DOMContentLoaded', function () {
    // Manejar el formulario de edición de grupo
    const editarForm = document.getElementById('grupoEditarForm');
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
                    .then(response => {
                        if (response.redirected) {
                            window.location.href = response.url;
                        } else {
                            return response.json();
                        }
                    })
                    .then(data => {
                        if (data && data.message) {
                            Swal.fire(
                                '¡Guardado!',
                                data.message,
                                'success'
                            ).then(() => {
                                window.location.href = '/grupos';
                            });
                        } else if (data && data.error) {
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

    // Manejar formularios de agregar usuario
    document.querySelectorAll('.agregar-form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Evita el envío del formulario

            fetch(form.action, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    Swal.fire(
                        '¡Agregado!',
                        data.message,
                        'success'
                    ).then(() => {
                        location.reload(); // Recargar la página después de agregar
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
                    'Hubo un problema al intentar agregar el usuario.',
                    'error'
                );
            });
        });
    });

    // Manejar formularios de remover usuario
    document.querySelectorAll('.remover-form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Evita el envío del formulario

            Swal.fire({
                title: '¿Estás seguro?',
                text: "No podrás revertir esto",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, remover'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(form.action, {
                        method: 'POST',
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            Swal.fire(
                                '¡Removido!',
                                data.message,
                                'success'
                            ).then(() => {
                                location.reload(); // Recargar la página después de remover
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
                            'Hubo un problema al intentar remover el usuario.',
                            'error'
                        );
                    });
                }
            });
        });
    });

    // Manejar formularios de eliminación de grupo
    document.querySelectorAll('.eliminar-form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Evita el envío del formulario

            Swal.fire({
                title: '¿Estás seguro?',
                text: "No podrás revertir esto",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminar'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(form.action, {
                        method: 'POST',
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            Swal.fire(
                                '¡Eliminado!',
                                data.message,
                                'success'
                            ).then(() => {
                                location.reload(); // Recargar la página después de eliminar
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
                            'Hubo un problema al intentar eliminar el grupo.',
                            'error'
                        );
                    });
                }
            });
        });
    });
});
