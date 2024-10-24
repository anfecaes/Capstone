document.addEventListener('DOMContentLoaded', function() {
    const chatBubble = document.getElementById('chatBubble');
    const chatWindow = document.getElementById('chatWindow');
    const chatMessages = document.getElementById('chatMessages');
    const userMessageInput = document.getElementById('userMessage');
    const sendButton = document.getElementById('sendButton');
    const back_elementbutton = document.getElementById("back_button");
    const cancel_elementbutton = document.getElementById("cancel_button");
    const send_elementbutton = document.getElementById("sendButton");
    const buttonContainer = document.getElementsByClassName("button-container")[0];

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

    function sendMessage(message) {
        if (!message) return;

        chatMessages.innerHTML += `<div class="user-message"><strong>Tú:</strong> ${message}</div>`;
        if ((userMessageInput.value).includes("pdf") || (userMessageInput.value).includes("pregunta")) {
            document.getElementsByClassName("button-container")[0].style.display="block";
            chatWindow.style.height = '650px';  // Expande el chat
            chatMessages.style.height = '500px'; // Expande el área de mensajes
        }
        userMessageInput.value = '';

        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.textContent = 'ASABOT está escribiendo...';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        fetch('ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            chatMessages.removeChild(typingIndicator);
            chatMessages.innerHTML += `<div class="bot-message"><strong>ASABOT:</strong> ${data.message}</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            chatMessages.removeChild(typingIndicator);
            chatMessages.innerHTML += `<div class="bot-message"><strong>Error:</strong> Hubo un problema al conectar con el chatbot.</div>`;
        });
    }

    cancel_elementbutton.onclick = function() {
        sendMessage("cancelar");
        chatWindow.style.height = '400px';  // Vuelve a la altura normal
        chatMessages.style.height = '300px'; // Vuelve a la altura normal de mensajes
        buttonContainer.style.display = "none"; // Oculta los botones
    };
    
    back_elementbutton.onclick = function() {
        sendMessage("volver");
    };
    
    send_elementbutton.onclick = function() {
        sendMessage(userMessageInput.value);
    };

    userMessageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage(userMessageInput.value);
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
