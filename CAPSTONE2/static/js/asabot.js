document.addEventListener('DOMContentLoaded', function() {
    const chatBubble = document.getElementById('chatBubble');
    const chatWindow = document.getElementById('chatWindow');
    const chatMessages = document.getElementById('chatMessages');
    const userMessageInput = document.getElementById('userMessage');

    // Mostrar/ocultar la ventana de chat al hacer clic en la burbuja
    chatBubble.addEventListener('click', () => {
        if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
            chatWindow.style.display = 'flex';
            if (!chatWindow.classList.contains('opened')) {
                chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> Bienvenido a AsaPeace, ¿en qué puedo ayudarte hoy?</div>`;
                chatWindow.classList.add('opened');
            }
        } else {
            chatWindow.style.display = 'none';
        }
    });

    // Función para obtener la ubicación del usuario
    function obtenerUbicacion() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitud = position.coords.latitude;
                    const longitud = position.coords.longitude;

                    // Enviar la ubicación al servidor
                    encontrarFunerariaCercana(latitud, longitud);
                },
                () => {
                    chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> No se pudo obtener tu ubicación. ¿En qué más puedo ayudarte?</div>`;
                }
            );
        } else {
            chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> Tu navegador no soporta la geolocalización. ¿En qué más puedo ayudarte?</div>`;
        }
    }

    // Función para encontrar la funeraria más cercana
    function encontrarFunerariaCercana(latitud, longitud) {
        fetch('ubicacion/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),  // Manejo del CSRF
            },
            body: JSON.stringify({
                latitud: latitud,
                longitud: longitud,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> ${data.error}</div>`;
            } else {
                chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> La funeraria más cercana es ${data.nombre}, ubicada en ${data.direccion}.</div>`;
            }
            chatMessages.scrollTop = chatMessages.scrollHeight;  // Desplazar hacia abajo
        })
        .catch((error) => {
            console.error('Error:', error);
            chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> Hubo un problema al buscar la funeraria cercana.</div>`;
        });
    }

    // Función para enviar el mensaje y hacer la petición a la API de OpenAI
    function sendMessage() {
        const userMessage = userMessageInput.value;

        if (userMessage.trim() === '') return;

        chatMessages.innerHTML += `<div class="user-message"><strong>Tú:</strong> ${userMessage}</div>`;
        userMessageInput.value = '';

        // Mostrar el indicador de que el bot está escribiendo
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.textContent = 'ASABOT está escribiendo...';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;  // Desplazar hacia abajo

        // Comprobar si el mensaje incluye "ubicación" para obtener la ubicación del usuario
        if (userMessage.toLowerCase().includes('ubicación')) {
            obtenerUbicacion();
            chatMessages.removeChild(typingIndicator); // Remover el indicador de escritura
            return; // Salir de la función para evitar llamar a la API de OpenAI
        }

        // Hacer la llamada a la API de OpenAI
        fetch('ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Remover el indicador de escritura
            chatMessages.removeChild(typingIndicator);

            // Mostrar la respuesta del bot
            chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> ${data.message}</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;  // Desplazar hacia abajo
        })
        .catch(error => {
            console.error('Error:', error);
            chatMessages.removeChild(typingIndicator);
            chatMessages.innerHTML += `<div class="bot-message"><strong>Error:</strong> Hubo un problema al conectar con el chatbot.</div>`;
        });
    }

    // Enviar mensaje al presionar Enter
    userMessageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

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
});
