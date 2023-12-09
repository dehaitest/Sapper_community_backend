document.addEventListener('DOMContentLoaded', function() {
    loadAgents();
    document.getElementById("agentCreationForm").addEventListener("submit", function(event) {
        event.preventDefault();
        createAgent();
    });
    document.getElementById("settingsCreationForm").addEventListener("submit", function(event) {
        event.preventDefault();
        updateSettings();
    });
    document.getElementById("userUuidForm").addEventListener("submit", async function(event) {
        event.preventDefault();
        await getAgentsByCreator();
    });
});
const accessToken = sessionStorage.getItem('accessToken');
function createAgent() {
    const agentName = document.getElementById('agentName').value;
    const agentDescription = document.getElementById('agentDescription').value;

    // Construct the data object
    const agentData = {
        name: agentName,
        description: agentDescription
    };

    fetch('/agents/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}` 
        },
        body: JSON.stringify(agentData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to create agent');
        }
    })
    .then(result => {
        console.log('Agent created:', result);
        // Optionally, update the UI to reflect the new agent
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateSettings() {
    const settingsId = document.getElementById('settingsId').value;
    const settingsModel = document.getElementById('settingsModel').value;
    const settingsOpenAIKey = document.getElementById('settingsOpenAIKey').value;

    // Construct the data object
    const settingsData = {
        model: settingsModel,
        openai_key: settingsOpenAIKey
    };

    fetch(`/settings/${settingsId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify(settingsData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to update settings');
        }
    })
    .then(result => {
        console.log('Settings updated:', result);
        // Optionally, update the UI to reflect the changes
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

async function getAgentsByCreator() {
    const userUuid = document.getElementById("userUuid").value;
    if (!userUuid) {
        alert("Please enter a User UUID");
        return;
    }

    try {
        const response = await fetch(`/agents/by-creator/${userUuid}`, {
            headers: {
                "Authorization": `Bearer ${accessToken}`  // Assuming accessToken is defined in your scope
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const agents = await response.json();
        console.log(agents)
        displayAgents(agents);  // Reuse the existing function to display agents
    } catch (error) {
        console.error('Error fetching agents:', error);
        alert("Failed to fetch agents for the given creator");
    }
}

async function loadAgents() {
    try {
        const response = await fetch('/agents/all', {
            headers: {
                "Authorization": `Bearer ${accessToken}` 
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const agents = await response.json();
        displayAgents(agents);
    } catch (error) {
        console.error('Error fetching agents:', error);
    }
}

function saveAgentDetails(event) {
    event.preventDefault();

    const agentId = document.getElementById("detailAgentId").value;
    const updatedAgent = {
        name: document.getElementById("detailName").value,
        image: document.getElementById("detailImage").value,
        spl: document.getElementById("detailSPL").value,
        spl_form: document.getElementById("detailSPLForm").value,
        nl: document.getElementById("detailNL").value,
        chain: document.getElementById("detailChain").value,
        settings: document.getElementById("detailSettings").value,
        active: document.getElementById("detailActive").checked
    };

    fetch(`/agents/${agentId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedAgent)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update the agent');
        }
        return response.json();
    })
    .then(() => {
        alert("Agent updated successfully");
        // Additional code to refresh the agent list and details
    })
    .catch(error => console.error("Error updating agent:", error));
}


function displayAgents(agents) {
    const container = document.getElementById('agentListContainer');
    container.innerHTML = ''; // Clear existing content

    agents.forEach(agent => {
        const agentDiv = document.createElement('div');
        agentDiv.className = 'agent-item';
        agentDiv.innerHTML = `
            <span class="agent-id">${agent.id}</span>
            <span class="agent-uuid">${agent.uuid}</span>
            <span class="agent-name">${agent.name}</span>
            <span class="agent-spl">${agent.spl}</span>
            <span class="agent-spl-form">${agent.spl_form}</span>
            <span class="agent-cfp">${agent.cfp}</span>
            <span class="agent-lint">${agent.lint}</span>
            <span class="agent-chain">${agent.chain}</span>
            <span class="agent-settings">${agent.settings_id}</span>
            <span class="agent-ownerUUID">${agent.owner_uuid}</span>
            <span class="agent-creatorUUID">${agent.creator_uuid}</span>
            <span class="agent-active">${agent.active ? 'Yes' : 'No'}</span>
            <span class="delete-icon" onclick="deleteAgent('${agent.uuid}')">🗑️</span>
        `;
        container.appendChild(agentDiv);
    });
}

async function deleteAgent(agentUUId) {
    try {
        const response = await fetch(`/agents/by-uuid/${agentUUId}`, {
            method: 'DELETE',
            headers: {
                "Authorization": `Bearer ${accessToken}` 
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        loadAgents(); // Refresh the list after deletion
    } catch (error) {
        console.error('Error deleting agent:', error);
    }
}
