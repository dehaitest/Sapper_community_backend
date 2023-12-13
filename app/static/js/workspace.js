document.addEventListener('DOMContentLoaded', function() {
    const accessToken = sessionStorage.getItem('accessToken');
    const agent_uuid = 'agent_j8xrtTsKeMJtG9jR'
    // Copilot
    // Input: plain text
    // Input example: "Please change the persona to computer science tutor."
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/formcopilot?token=${accessToken}&agent_uuid=${agent_uuid}`, 'Copilot');

    // CFP
    // Input: No need input, any char
    // Input example: "1"
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/splformtocfp?token=${accessToken}&agent_uuid=${agent_uuid}`, 'CFP');

    // Linting
    // Input: No need input, any char
    // Input example: "1"
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/splformlint?token=${accessToken}&agent_uuid=${agent_uuid}`, 'Lint');

    // Emulator
    // Input: Json string {"message": String data, "file_ids": List of strings}
    // Input example: {"message": "How can I solve the problem show in the file?", "file_ids": ["dafasa", "asdfasf"]}
    let isNewChat = false; // or false, depending on your logic
    let newChatParam = isNewChat ? "True" : "False";
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/splemulator?token=${accessToken}&agent_uuid=${agent_uuid}&new_chat=${newChatParam}`, 'Emulator');

    // Compiler
    // Input: No need input, any char
    // Input example: "1"
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/splcompiler?token=${accessToken}&agent_uuid=${agent_uuid}`, 'Compiler');

    // Chain running
    // Input: Json string {"message": String data, "file_ids": List of strings, "mode": "CONTINUE" or "RUN_NEXT"}
    // Input example: {"message": "user input message", "file_ids": ["dafasa", "asdfasf"], "mode": "CONTINUE"}
    // Input example: {"message": "user input message", "file_ids": ["dafasa", "asdfasf"], "mode": "RUN_NEXT", "step_id": 0}
    // Input example: {"message": "", "file_ids": [], "mode": "RUN_NEXT", "step_id": 1} 
    // Note: If this is not the first message for "RUN_NEXT" mode, and if user input message and upload new files, just use the new message and file, if user doesn't input anything, you just leave them empty.
    // Remember to edit the step_id for the "RUN_NEXT". You can get the step_id from last returned message.
    isNewChat = false; // or false, depending on your logic
    newChatParam = isNewChat ? "True" : "False";
    initializeChatbot(`ws://localhost:8000/ws/sapperchain/runchain?token=${accessToken}&agent_uuid=${agent_uuid}&new_chat=${newChatParam}`, 'RunChain');

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
