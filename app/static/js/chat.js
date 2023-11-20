document.addEventListener('DOMContentLoaded', (event) => {
    const ws = new WebSocket(`wss://${window.location.host}/ws/chat`);
    const messagesContainer = document.getElementById('messages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatContainer = document.getElementById('chat-container');
    let chatbotMessageContainer = null;
    let chatbotOriginalText = "";  // Store the original Markdown text

    function addMessage(content, byUser) {    
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = marked.parse(content); // Parse Markdown to HTML
        messageDiv.classList.add('message', byUser ? 'user-message' : 'server-message');
        messagesContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    ws.onmessage = function(event) {
        // Handle incoming message from WebSocket
        if (event.data === "__END_OF_RESPONSE__") {
            chatbotMessageContainer = null;
            chatbotOriginalText = ""; // Reset the original text
        } else {
            if (!chatbotMessageContainer) {
                chatbotMessageContainer = document.createElement('div');
                chatbotMessageContainer.classList.add('message', 'server-message');
                messagesContainer.appendChild(chatbotMessageContainer);
            }
            chatbotOriginalText += event.data;
            chatbotMessageContainer.innerHTML = marked.parse(chatbotOriginalText);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    };

    sendButton.addEventListener('click', function() {
        sendMessage();
    });

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, true); // true for user messages
            ws.send(message);
            messageInput.value = '';
        }
    }
});
