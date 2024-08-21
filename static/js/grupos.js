'use strict';

document.addEventListener('DOMContentLoaded', function () {
    
    // Manejar el formulario de creación de grupo
    const crearForm = document.getElementById('grupoCrearForm');
    if (crearForm) {
        crearForm.addEventListener('submit', function (event) {
            // Evita el envío del formulario
            event.preventDefault();

            // Obtener los valores de los campos de tiempo
            const onTime = parseInt(document.getElementById('on_time').value);
            const runningLate = parseInt(document.getElementById('running_late').value);
            const isLate = parseInt(document.getElementById('is_late').value);

            // Validar la lógica de los tiempos
            if (onTime >= runningLate || runningLate >= isLate) {
                Swal.fire(
                    'Error',
                    'Los tiempos de SLA deben cumplir con la siguiente lógica: On Time < Running Late < Is Late',
                    'error'
                );
                return;
            }

            Swal.fire({
                title: '¿Estás seguro?',
                text: "¿Quieres crear este grupo?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, crear grupo'
            }).then((result) => {
                if (result.isConfirmed) {
                    const formData = new FormData(crearForm);

                    fetch(crearForm.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        } else {
                            return response.json().then(data => {
                                throw new Error(data.error || 'Error desconocido');
                            });
                        }
                    })
                    .then(data => {
                        if (data.message) {
                            Swal.fire(
                                '¡Creado!',
                                data.message,
                                'success'
                            ).then(() => {
                                window.location.href = '/grupos';
                            });
                        } else if (data.error) {
                            Swal.fire(
                                'Error',
                                data.error,
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error.message);
                        Swal.fire(
                            'Error',
                            error.message || 'Hubo un problema al intentar crear el grupo.',
                            'error'
                        );
                    });
                }
            });
        });
    }
    // Manejar el formulario de edición de grupo
    // Manejar el formulario de edición de grupo
const editarForm = document.getElementById('grupoEditarForm');
if (editarForm) {
    editarForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Evita el envío del formulario

        // Obtener los valores de los campos de tiempo
        const onTime = parseInt(document.getElementById('on_time').value);
        const runningLate = parseInt(document.getElementById('running_late').value);
        const isLate = parseInt(document.getElementById('is_late').value);

        // Validar la lógica de los tiempos
        if (onTime >= runningLate || runningLate >= isLate) {
            Swal.fire(
                'Error',
                'Los tiempos de SLA deben cumplir con la siguiente lógica: On Time < Running Late < Is Late',
                'error'
            );
            return;
        }

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
                            window.location.href = '/grupos';
                        });
                    } else if (data.error) {
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
                } else if (data.error) {
                    Swal.fire(
                        'Error',
                        data.error,
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
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
                        } else if (data.error) {
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
                                window.location.href = '/grupos'; // Redirige después de eliminar
                            });
                        } else if (data.error) {
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
