async function publishWechat() {
    publish('/sapperchain/publish/wechat');
}

async function publishRobot() {
    publish('/sapperchain/publish/robot');
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
