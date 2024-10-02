let mapa; 

// Función para inicializar el mapa
function inicializarMapa(latitud, longitud) {
    // Si el mapa ya fue inicializado, simplemente actualiza la vista
    if (mapa) {
        mapa.setView([latitud, longitud], 13);
        return;
    }

    // Crear el mapa y centrarlo en la ubicación obtenida
    mapa = L.map('map').setView([latitud, longitud], 13);

    // Añadir capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapa);

    // Estilos personalizados para el marcador
    let iconoUsuario = L.icon({
        iconUrl: 'static/images/pajaroubi.png', // Reemplaza con la ruta a tu icono personalizado
        iconSize: [38, 38], // Tamaño del icono
        iconAnchor: [19, 38], // Ancla del icono
        popupAnchor: [0, -38] // Ancla del popup
    });

    // Añadir un marcador en la ubicación del usuario
    L.marker([latitud, longitud], { icon: iconoUsuario }).addTo(mapa)
        .bindPopup('Tu ubicación actual')
        .openPopup();
}

// Función para obtener la ubicación del usuario
function obtenerUbicacion() {
    if (navigator.geolocation) {
        console.log("Obteniendo la ubicación...");
        navigator.geolocation.getCurrentPosition(mostrarPosicion, mostrarError);
    } else {
        alert("La geolocalización no es soportada por este navegador.");
    }
}

// Función que maneja la posición obtenida
function mostrarPosicion(position) {
    let latitud = position.coords.latitude;
    let longitud = position.coords.longitude;
    console.log("Latitud: " + latitud + " Longitud: " + longitud);

    // Inicializar el mapa con la ubicación del usuario
    inicializarMapa(latitud, longitud);

    // Aquí puedes hacer una llamada AJAX para enviar la ubicación al servidor
    enviarUbicacionAlServidor(latitud, longitud);
}

// Función para mostrar errores de geolocalización
function mostrarError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("El usuario denegó la solicitud de geolocalización.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("La información de ubicación no está disponible.");
            break;
        case error.TIMEOUT:
            alert("La solicitud de ubicación ha expirado.");
            break;
        case error.UNKNOWN_ERROR:
            alert("Se produjo un error desconocido.");
            break;
    }
}

// Función para enviar las coordenadas al servidor
function enviarUbicacionAlServidor(latitud, longitud) {
    fetch('/ubicacion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de manejar CSRF correctamente
        },
        body: JSON.stringify({
            latitud: latitud,
            longitud: longitud
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Éxito:', data);
        // Aquí puedes hacer algo con la respuesta del servidor
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Inicializa la obtención de la ubicación cuando se carga la página
window.onload = obtenerUbicacion;

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprueba si esta cookie contiene el nombre que estamos buscando
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
