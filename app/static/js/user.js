document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("createUserForm").addEventListener("submit", function(event) {
        event.preventDefault();
        createUser();
    });

    document.getElementById("getUserForm").addEventListener("submit", function(event) {
        event.preventDefault();
        getUser();
    });
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        login();
    });
    document.getElementById('refreshTokenButton').addEventListener('click', function(event) {
        refreshAccessToken();
    });
});

function createUser() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("/users/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, password })
    })
    .then(response => response.json())
    .then(data => showResult(data))
    .catch(error => console.error("Error:", error));
}

function getUser() {
    const userId = document.getElementById("userId").value;

    fetch("/users/" + userId)
    .then(response => response.json())
    .then(data => showResult(data))
    .catch(error => console.error("Error:", error));
}

function showResult(data) {
    const resultDiv = document.getElementById("result");
    resultDiv.textContent = JSON.stringify(data, null, 2);
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': email,
                'password': password
            })
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        sessionStorage.setItem('accessToken', data.token.access_token);
        document.getElementById('result').textContent = 'Login successful. Token: ' + data.token.access_token;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'Login failed';
    }
}

async function refreshAccessToken() {
    try {
        const response = await fetch('/users/refreshtoken', {
            method: 'POST',
            credentials: 'include', // Include cookies in the request
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('New Access Token:', data.access_token);

        // Save the new access token for future requests
        sessionStorage.setItem('accessToken', data.access_token);

        // Update the UI or inform the user
        document.getElementById('result').textContent = 'Token refreshed successfully.' + data.access_token;
    } catch (error) {
        console.error('Error refreshing access token:', error);
        document.getElementById('result').textContent = 'Error refreshing token.';
    }
}