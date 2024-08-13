'use strict';

// Password reset

(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const passwordForm = document.querySelector('form#password-reset-form');

        passwordForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(passwordForm);
            const url = passwordForm.getAttribute('action') || window.location.href;

            fetch(url, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    let successTimerInterval;
                    Swal.fire({
                        title: '¡Éxito!',
                        text: data.message,
                        timer: 2000, // 2 segundos
                        timerProgressBar: true,
                        didOpen: () => {
                            Swal.showLoading();
                            successTimerInterval = setInterval(() => {
                                const content = Swal.getContent();
                                if (content) {
                                    const timerElement = content.querySelector('b');
                                    if (timerElement) {
                                        timerElement.textContent = Swal.getTimerLeft();
                                    }
                                }
                            }, 100);
                        },
                        willClose: () => {
                            clearInterval(successTimerInterval);
                        }
                    }).then((result) => {
                        if (result.dismiss === Swal.DismissReason.timer) {
                            window.location.href = '/dashboard';  // Redirigir después de éxito
                        }
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: '¡Error!',
                        text: data.message,
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message || 'Ocurrió un error al procesar la solicitud.',
                });
            });
        });
    });
})();

// Password reset request

(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const recoveryForm = document.querySelector('form#password-recovery-form');

        recoveryForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(recoveryForm);
            const url = recoveryForm.getAttribute('action') || window.location.href;

            fetch(url, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    let successTimerInterval;
                    Swal.fire({
                        title: '¡Éxito!',
                        text: data.message,
                        timer: 10000, // 10 segundos
                        timerProgressBar: true,
                        didOpen: () => {
                            Swal.showLoading();
                            successTimerInterval = setInterval(() => {
                                const content = Swal.getContent();
                                if (content) {
                                    const timerElement = content.querySelector('b');
                                    if (timerElement) {
                                        timerElement.textContent = Swal.getTimerLeft();
                                    }
                                }
                            }, 100);
                        },
                        willClose: () => {
                            clearInterval(successTimerInterval);
                        }
                    }).then((result) => {
                        if (result.dismiss === Swal.DismissReason.timer) {
                            window.location.href = '/login';  // Redirigir después de éxito
                        }
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: '¡Error!',
                        text: data.message,
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message || 'Ocurrió un error al procesar la solicitud.',
                });
            });
        });
    });
})();
