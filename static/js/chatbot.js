async function sendMessage() {

    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (message === '') return;

    const chat = document.getElementById('chatMessages');

    // MENSAJE USUARIO
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');
    userMessage.textContent = message;
    chat.appendChild(userMessage);

    input.value = '';

    try {

        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: message
            })
        });

        const data = await response.json();

        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');
        botMessage.textContent = data.respuesta;

        chat.appendChild(botMessage);

        chat.scrollTop = chat.scrollHeight;

    } catch (error) {

        const errorMessage = document.createElement('div');
        errorMessage.classList.add('message', 'bot');
        errorMessage.textContent = 'Error al conectar con Flask.';

        chat.appendChild(errorMessage);
    }
}

// ENTER

document.getElementById('userInput').addEventListener('keypress', function(e) {

    if (e.key === 'Enter') {
        sendMessage();
    }

});