document.addEventListener('DOMContentLoaded', function() {
    loadAgents();
});

async function loadAgents() {
    try {
        const response = await fetch('/agents/all');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const agents = await response.json();
        displayAgents(agents);
    } catch (error) {
        console.error('Error fetching agents:', error);
    }
}

function displayAgents(agents) {
    const container = document.getElementById('agentListContainer');
    container.innerHTML = ''; // Clear existing content

    agents.forEach(agent => {
        const agentDiv = document.createElement('div');
        agentDiv.className = 'agent-item';
        agentDiv.innerHTML = `
            <span class="agent-id">${agent.id}</span>
            <span class="agent-name">${agent.name}</span>
            <span class="agent-image">${agent.image}</span>
            <span class="agent-spl">${agent.spl}</span>
            <span class="agent-spl-form">${agent.spl_form}</span>
            <span class="agent-nl">${agent.nl}</span>
            <span class="agent-chain">${agent.chain}</span>
            <span class="agent-settings">${agent.settings}</span>
            <span class="agent-created-by">${agent.created_by}</span>
            <span class="agent-create-datetime">${agent.create_datetime}</span>
            <span class="agent-update-datetime">${agent.update_datetime}</span>
            <span class="agent-active">${agent.active ? 'Yes' : 'No'}</span>
            <span class="delete-icon" onclick="deleteAgent(${agent.id})">🗑️</span>
        `;
        container.appendChild(agentDiv);
    });
}

async function deleteAgent(agentId) {
    try {
        const response = await fetch(`/agents/${agentId}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        loadAgents(); // Refresh the list after deletion
    } catch (error) {
        console.error('Error deleting agent:', error);
    }
}
