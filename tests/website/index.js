let items = [
    { name: "Item 1", description: "Description of Item 1" },
    { name: "Item 2", description: "Description of Item 2" },
    // ... more items
];

// Function to display items
function displayItems(items) {
    const itemsList = document.getElementById("itemsList");
    itemsList.innerHTML = ""; // Clear the list first

    // Append each item to the list
    items.forEach(item => {
        let div = document.createElement("div");
        div.innerHTML = `<h2>${item.name}</h2><p>${item.description}</p >`;
        itemsList.appendChild(div);
    });
}

// Initial display of items
displayItems(items);

// Function to perform search
function performSearch() {
    let searchTerm = document.getElementById("searchBar").value.toLowerCase();

    // Filter items based on search term
    let filteredItems = items.filter(item => 
        item.name.toLowerCase().includes(searchTerm) || 
        item.description.toLowerCase().includes(searchTerm));

    displayItems(filteredItems);
}