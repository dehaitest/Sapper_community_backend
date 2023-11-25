document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("createUserForm").addEventListener("submit", function(event) {
        event.preventDefault();
        createUser();
    });

    document.getElementById("getUserForm").addEventListener("submit", function(event) {
        event.preventDefault();
        getUser();
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
