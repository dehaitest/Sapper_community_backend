document.addEventListener('DOMContentLoaded', function() {
    const accessToken = sessionStorage.getItem('accessToken');
    const agent_uuid = 'agent_5I43F3Chmpz5wMok'
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/formcopilot?token=${accessToken}&agent_uuid=${agent_uuid}`, 'Chatbot 1');
    // Add more chatbots here, e.g., initializeChatbot('wss://anotherendpoint', 'Chatbot 2');
});

function initializeChatbot(endpoint, chatbotName) {

    const chatbotContainer = document.createElement('div');
    chatbotContainer.classList.add('chatbot-container');

    const chatbotTitle = document.createElement('h2');
    chatbotTitle.textContent = chatbotName;
    chatbotTitle.classList.add('chatbot-title');
    chatbotContainer.appendChild(chatbotTitle);

    const chatContainer = document.createElement('div');
    chatContainer.classList.add('chat-container');

    const inputContainer = document.createElement('div');
    inputContainer.classList.add('input-container');

    const messageInput = document.createElement('input');
    messageInput.type = 'text';
    messageInput.classList.add('message-input');

    const sendButton = document.createElement('button');
    sendButton.textContent = 'Send';
    sendButton.classList.add('send-button');

    inputContainer.appendChild(messageInput);
    inputContainer.appendChild(sendButton);
    chatbotContainer.appendChild(chatContainer);
    chatbotContainer.appendChild(inputContainer);
    document.getElementById('chatbots-container').appendChild(chatbotContainer);

    const ws = new WebSocket(endpoint);

    ws.onopen = function(event) {
        console.log(`${chatbotName} connected to WebSocket`);
    };

    ws.onmessage = function(event) {
        const data = event.data;
        const messageElement = document.createElement('div');
        messageElement.classList.add('server-message');
        messageElement.textContent = data.copilot || data;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    sendButton.onclick = function() {
        const message = messageInput.value;
        if (message) {
            ws.send(message);
            const messageElement = document.createElement('div');
            messageElement.classList.add('user-message');
            messageElement.textContent = message;
            chatContainer.appendChild(messageElement);
            messageInput.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    };

    ws.onerror = function(event) {
        console.error("WebSocket error observed:", event);
    };

    ws.onclose = function(event) {
        console.log(`${chatbotName} WebSocket connection closed:`, event);
    };
}
