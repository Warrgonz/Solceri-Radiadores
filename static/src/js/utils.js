'use strict';

// Obtenemos la URL de la página actual
var currentUrl = window.location.href;

// URL contiene '/dashboard'
if (currentUrl.includes('/dashboard')) {
    document.querySelector('.sidebar-item:nth-child(2)').classList.add('active');
} else if (currentUrl.includes('/tiquetes')) {
    // URL contiene '/tiquetes'
    document.querySelector('.sidebar-item:nth-child(3)').classList.add('active');
} else if (currentUrl.includes('/usuarios')) {
    // URL contiene '/usuarios'
    document.querySelector('.sidebar-item:nth-child(4)').classList.add('active');
} else if (currentUrl.includes('/equipos')) {
    // URL contiene '/equipos'
    document.querySelector('.sidebar-item:nth-child(5)').classList.add('active');
} else if (currentUrl.includes('/vacaciones')) {
    // URL contiene '/vacaciones'
    document.querySelector('.sidebar-item:nth-child(6)').classList.add('active');
} else if (currentUrl.includes('/categorias')) {
    // URL contiene '/categorias'
    document.querySelector('.sidebar-item:nth-child(7)').classList.add('active');
} else if (currentUrl.includes('/catalogo')) {
    // URL contiene '/catalogo'
    document.querySelector('.sidebar-item:nth-child(8)').classList.add('active');
} else if (currentUrl.includes('/cotizaciones')) {
    // URL contiene '/cotizaciones'
    document.querySelector('.sidebar-item:nth-child(9)').classList.add('active');
} else if (currentUrl.includes('/reportes')) {
    // URL contiene '/reportes'
    document.querySelector('.sidebar-item:nth-child(10)').classList.add('active');
}

