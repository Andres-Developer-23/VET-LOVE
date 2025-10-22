// JavaScript para el chat con veterinario IA

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const mensajeInput = document.getElementById('mensaje-input');
    const enviarBtn = document.getElementById('enviar-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Auto-scroll al final de los mensajes
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Scroll inicial
    scrollToBottom();

    // Función para mostrar mensaje de carga
    function mostrarMensajeCarga() {
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'message message-assistant';
        loadingMessage.id = 'loading-message';
        // Variar el mensaje de escritura para que parezca más humano
        const typingMessages = [
            "Escribiendo",
            "Pensando en tu mascota",
            "Recordando casos similares",
            "Consultando mis notas"
        ];
        const randomMessage = typingMessages[Math.floor(Math.random() * typingMessages.length)];

        loadingMessage.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user-md"></i>
            </div>
            <div class="message-content">
                <div class="message-text">
                    <span class="loading-dots">${randomMessage}</span>
                </div>
            </div>
        `;
        chatMessages.appendChild(loadingMessage);
        scrollToBottom();
        return loadingMessage;
    }

    // Función para agregar mensaje al chat
    function agregarMensaje(contenido, rol, tiempo = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${rol}`;

        const now = new Date();
        const timeString = tiempo || now.toLocaleTimeString('es-CO', {
            hour: '2-digit',
            minute: '2-digit'
        });

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-${rol === 'user' ? 'user' : 'user-md'}"></i>
            </div>
            <div class="message-content">
                <div class="message-text">${contenido.replace(/\n/g, '<br>')}</div>
                <small class="message-time">${timeString}</small>
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    }

    // Función para enviar mensaje
    async function enviarMensaje(mensaje) {
        try {
            // Mostrar mensaje del usuario
            agregarMensaje(mensaje, 'user');

            // Limpiar input
            mensajeInput.value = '';
            enviarBtn.disabled = true;
            mensajeInput.disabled = true;

            // Mostrar mensaje de carga
            const loadingMessage = mostrarMensajeCarga();

            // Simular tiempo de "pensamiento" humano (1-3 segundos aleatorios)
            const thinkingDelay = Math.random() * 2000 + 1000; // 1-3 segundos
            await new Promise(resolve => setTimeout(resolve, thinkingDelay));

            // Enviar a la API
            const response = await fetch('/chat/enviar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ mensaje: mensaje })
            });

            // Remover mensaje de carga
            loadingMessage.remove();

            if (response.ok) {
                const data = await response.json();
                agregarMensaje(data.respuesta, 'assistant');
            } else {
                const errorData = await response.json();
                // Mostrar error con indicador de escribiendo
                const errorLoading = mostrarMensajeCarga();
                setTimeout(() => {
                    errorLoading.remove();
                    agregarMensaje(`Error: ${errorData.error || 'Error desconocido'}`, 'assistant');
                }, 500);
            }

        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            // Remover mensaje de carga si existe
            const loadingMsg = document.getElementById('loading-message');
            if (loadingMsg) loadingMsg.remove();

            // Mostrar mensaje de error con indicador de escribiendo
            const errorLoading = mostrarMensajeCarga();
            setTimeout(() => {
                errorLoading.remove();
                agregarMensaje('Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.', 'assistant');
            }, 500);
        } finally {
            // Re-habilitar input y botón
            enviarBtn.disabled = false;
            mensajeInput.disabled = false;
            mensajeInput.focus();
        }
    }

    // Event listener para el formulario
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const mensaje = mensajeInput.value.trim();
        if (mensaje) {
            enviarMensaje(mensaje);
        }
    });

    // Event listener para Enter (sin Shift)
    mensajeInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const mensaje = mensajeInput.value.trim();
            if (mensaje && !enviarBtn.disabled) {
                enviarMensaje(mensaje);
            }
        }
    });

    // Event listener para cambios en el input
    mensajeInput.addEventListener('input', function() {
        const mensaje = this.value.trim();
        enviarBtn.disabled = !mensaje || this.disabled;
    });

    // Focus inicial en el input
    mensajeInput.focus();

    // Mostrar notificación de bienvenida si no hay mensajes previos
    const existingMessages = chatMessages.querySelectorAll('.message').length;
    if (existingMessages === 0) {
        setTimeout(async () => {
            let mensajeBienvenida;

            if (esPrimeraVez) {
                // Primer saludo para nuevos usuarios
                mensajeBienvenida = `¡Hola ${nombreUsuario}! 🐾 Bienvenido a ${nombreVeterinaria}. Soy Ana, veterinaria. ¿En qué puedo ayudarte con tu mascota hoy?`;
            } else {
                // Saludo de retorno para usuarios recurrentes
                mensajeBienvenida = `¡Hola de nuevo ${nombreUsuario}! 🐾 Soy Ana de ${nombreVeterinaria}. ¿Cómo está tu mascota? ¿En qué puedo ayudarte hoy?`;
            }

            // Mostrar indicador de escribiendo antes del mensaje de bienvenida
            const loadingMessage = mostrarMensajeCarga();

            // Simular tiempo de escritura
            const typingDelay = Math.random() * 1500 + 500; // 0.5-2 segundos
            await new Promise(resolve => setTimeout(resolve, typingDelay));

            // Remover indicador y mostrar mensaje
            loadingMessage.remove();
            agregarMensaje(mensajeBienvenida, 'assistant');
        }, 1000);
    }

    console.log('Chat con veterinario IA inicializado correctamente');
});