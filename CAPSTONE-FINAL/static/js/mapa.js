// Variables globales para manejar el marcador de la ubicación del usuario y el infowindow
let userMarker = null;
let infoWindow = null;
let directionsRenderer = null; // Para mostrar las direcciones en el mapa
let map = null; // Variable global para el mapa

// Función para inicializar el mapa con la ubicación del usuario
function initMap(position) {
    const userLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
    };

    // Crear el mapa centrado en la ubicación del usuario
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: userLocation,
    });

    // Agregar un marcador para la ubicación del usuario con un ícono distintivo
    userMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        title: "Tu ubicación actual",
        icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png', // Ícono azul para el usuario
    });

    // Crear el infowindow
    infoWindow = new google.maps.InfoWindow();

    // Crear un objeto PlacesService para buscar lugares cercanos
    const service = new google.maps.places.PlacesService(map);

    // Configuración de la solicitud para buscar funerarias cercanas
    const request = {
        location: userLocation,  // Ubicación actual del usuario
        radius: 5000,  // Radio de búsqueda en metros (5 km)
        type: ['funeral_home'],  // Tipo de lugar que estamos buscando: funerarias
    };

    // Realizar la búsqueda de funerarias cercanas
    service.nearbySearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            results.forEach((place) => {
                // Crear un marcador para cada funeraria encontrada
                const placeMarker = new google.maps.Marker({
                    position: place.geometry.location,
                    map: map,
                    title: place.name,
                    icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png', // Ícono rojo para las funerarias
                });

                // Mostrar información adicional al hacer clic en el marcador
                const contentString = `
                    <h4>${place.name}</h4>
                    <p>${place.vicinity}</p>
                    <button onclick="getDirections(${place.geometry.location.lat()}, ${place.geometry.location.lng()})">Cómo llegar</button>
                `;

                // Asociar el evento de clic al marcador de la funeraria
                placeMarker.addListener('click', () => {
                    infoWindow.setContent(contentString);
                    infoWindow.open(map, placeMarker);

                    // Cerrar el infowindow anterior (si existe)
                    if (infoWindow) {
                        infoWindow.close();
                    }
                    infoWindow.open(map, placeMarker);
                });
            });
        } else {
            console.error('Error al buscar funerarias: ' + status);
        }
    });
}

// Función para manejar los errores de geolocalización
function handleLocationError(browserHasGeolocation) {
    const defaultLocation = { lat: -33.4489, lng: -70.6693 }; // Coordenadas de Santiago (ubicación predeterminada)

    const mapOptions = {
        zoom: 12,
        center: defaultLocation,
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    userMarker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        title: "Ubicación predeterminada: Santiago de Chile",
        icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png', // Ícono azul para la ubicación predeterminada
    });

    console.error(
        browserHasGeolocation
            ? "Error: No se pudo obtener la ubicación."
            : "Error: Tu navegador no soporta la geolocalización."
    );
}

// Función para obtener direcciones hacia la funeraria seleccionada
function getDirections(destinationLat, destinationLng) {
    // Obtener la ubicación del usuario directamente
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };

            // Crear el servicio de direcciones
            const directionsService = new google.maps.DirectionsService();

            // Limpiar la ruta anterior si existe
            if (directionsRenderer) {
                directionsRenderer.setDirections({ routes: [] });
            }

            directionsRenderer = new google.maps.DirectionsRenderer({
                map: map
            });

            const request = {
                origin: userLocation,
                destination: { lat: destinationLat, lng: destinationLng },
                travelMode: google.maps.TravelMode.TRANSIT,  // Usar transporte público
            };

            // Solicitar direcciones
            directionsService.route(request, (response, status) => {
                if (status === google.maps.DirectionsStatus.OK) {
                    directionsRenderer.setDirections(response);

                    // Extraer detalles del viaje en transporte público (micro, metro)
                    const steps = response.routes[0].legs[0].steps;
                    let transitDetails = 'Direcciones para transporte público:\n';

                    steps.forEach((step, index) => {
                        if (step.transit) {
                            const line = step.transit.line;
                            transitDetails += `Paso ${index + 1}: Toma la línea ${line.name} (${line.vehicle.type}) en dirección a ${line.destinationName}. Duración estimada: ${step.duration.text}.\n`;
                        }
                    });

                    // Mostrar detalles del transporte público en consola
                    console.log(transitDetails);
                } else {
                    console.error('Error al obtener direcciones: ' + status);
                }
            });
        }, () => {
            console.error("No se pudo obtener la ubicación del usuario.");
        });
    } else {
        console.error("La geolocalización no está soportada por tu navegador.");
    }
}

// Esperar a que la API de Google Maps y el DOM estén completamente cargados antes de inicializar el mapa
window.addEventListener('load', () => {
    if (typeof google !== 'undefined' && google.maps) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    initMap(position);
                },
                () => handleLocationError(true)
            );
        } else {
            handleLocationError(false);
        }
    } else {
        console.error('Google Maps no se ha cargado correctamente.');
    }
});
