document.addEventListener("DOMContentLoaded", function() {
    // Load prompts when the page is loaded
    loadPrompts();

    // Event listeners for forms
    document.getElementById("createPromptForm").addEventListener("submit", createPrompt);
    document.getElementById("editPromptDetailsForm").addEventListener("submit", savePromptDetails);

    let link = document.createElement('link');
    link.rel = 'icon';
    link.href = '/favicon.ico';
    link.type = 'image/x-icon';
    document.getElementsByTagName('head')[0].appendChild(link);
});

// Function to load and display prompts
function loadPrompts() {
    fetch('/prompts/all') 
        .then(response => response.json())
        .then(prompts => {
            const promptListContainer = document.getElementById("promptListContainer");
            promptListContainer.innerHTML = ''; // Clear existing content

            prompts.forEach(prompt => {
                // Create a container for each prompt item
                const promptDiv = document.createElement("div");
                promptDiv.className = "prompt-item";

                // Create and append the prompt name element
                const promptNameSpan = document.createElement("span");
                promptNameSpan.className = "prompt-name";
                promptNameSpan.textContent = prompt.name;
                promptNameSpan.onclick = () => loadPromptDetails(prompt.id);
                promptDiv.appendChild(promptNameSpan);

                // Create and append the prompt description element
                const promptDescriptionSpan = document.createElement("span");
                promptDescriptionSpan.className = "prompt-description";
                promptDescriptionSpan.textContent = prompt.description;
                promptDiv.appendChild(promptDescriptionSpan);

                // Create and append the delete icon
                const deleteIconSpan = document.createElement("span");
                deleteIconSpan.className = "delete-icon";
                deleteIconSpan.innerHTML = "🗑️"; // Using an emoji as the icon
                deleteIconSpan.onclick = () => deletePrompt(prompt.id); // Implement the deletePrompt function
                promptDiv.appendChild(deleteIconSpan);

                promptListContainer.appendChild(promptDiv);
            });
        })
        .catch(error => console.error("Error loading prompts:", error));
}


// Function to load details of a prompt
function loadPromptDetails(promptId) {
    fetch(`/prompts/by-id/${promptId}`)
        .then(response => response.json())
        .then(prompt => {
            document.getElementById("detailPromptId").value = prompt.id;
            document.getElementById("detailName").value = prompt.name;
            document.getElementById("detailPromptText").value = prompt.prompt;
            document.getElementById("detailDescription").value = prompt.description;
            document.getElementById("detailCreateDate").value = prompt.create_datetime;
            document.getElementById("detailUpdateDate").value = prompt.update_datetime;
            document.getElementById("detailActive").checked = prompt.active;
        })
        .catch(error => console.error("Error loading prompt details:", error));
}

// Function to save prompt details
function savePromptDetails(event) {
    event.preventDefault();

    const promptId = document.getElementById("detailPromptId").value;
    const updatedPrompt = {
        name: document.getElementById("detailName").value,
        prompt: document.getElementById("detailPromptText").value,
        description: document.getElementById("detailDescription").value,
        isActive: document.getElementById("detailActive").checked
    };

    fetch(`/prompts/${promptId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedPrompt)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update the prompt');
        }
        return response.json();
    })
    .then(() => {
        alert("Prompt updated successfully");
        loadPrompts(); // Refresh the list of prompts
        loadPromptDetails(promptId); // Refresh the details section
    })
    .catch(error => console.error("Error updating prompt:", error));
}

// Function to create a new prompt
function createPrompt(event) {
    event.preventDefault();

    const newPrompt = {
        name: document.getElementById("newName").value,
        prompt: document.getElementById("newPromptText").value,
        description: document.getElementById("newDescription").value
    };

    fetch('/prompts/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newPrompt)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to create a new prompt');
        }
        return response.json();
    })
    .then(() => {
        alert("New prompt created successfully");
        loadPrompts(); // Refresh the list of prompts
    })
    .catch(error => console.error("Error creating prompt:", error));
}

// Function to delete a prompt
function deletePrompt(promptId) {
    if (!confirm("Are you sure you want to delete this prompt?")) {
        return; // Do nothing if the user cancels the confirmation dialog
    }

    fetch(`/prompts/${promptId}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                alert("Prompt deleted successfully");
                loadPrompts(); // Refresh the list of prompts
            } else {
                alert("Failed to delete the prompt");
            }
        })
        .catch(error => {
            console.error("Error deleting prompt:", error);
            alert("An error occurred while deleting the prompt");
        });
}

