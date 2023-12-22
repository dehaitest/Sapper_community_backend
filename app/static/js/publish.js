document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("websiteForm").addEventListener("submit", async function(event) {
        event.preventDefault();
        await SentWebsiteRequest();
    });  
});

async function publishWechat() {
    publish('/sapperchain/publish/wechat');
}

async function publishRobot() {
    publish('/sapperchain/publish/robot');
}

async function publishWebsite() {
    publish('/sapperchain/publish/website');
}
const accessToken = sessionStorage.getItem('accessToken');
async function publish(endpoint) {
    const agentUuid = document.getElementById('agentUuid').value;

    const data = {
        accessToken: accessToken,
        agentUuid: agentUuid
    };

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify(data)
        });

        const resultText = await response.text();
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = resultText; 
    } catch (error) {
        document.getElementById('result').innerText = 'Error: ' + error.message;
    }
}

async function SentWebsiteRequest() {
    const agent_uuid = document.getElementById('agent_uuid').value;
    const instruction = document.getElementById('instruction').value;
    const user_input = document.getElementById('user_input').value;
    const url = `/client/website?agent_uuid=${encodeURIComponent(agent_uuid)}&instruction=${encodeURIComponent(instruction)}`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'body': user_input,
            })
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        document.getElementById('result').textContent = data;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'Error';
    }
}
