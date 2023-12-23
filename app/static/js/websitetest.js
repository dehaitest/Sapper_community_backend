$(document).ready(function(){
    // Initialize all products
    let allProducts = [
      {"ProductName": "Building Blocks Set","ProductDescription": "A creative set of colorful building blocks to inspire imaginative play and problem-solving skills.","ProductPrice": "$19.99"},
      {"ProductName": "Stuffed Teddy Bear","ProductDescription": "A soft and cuddly teddy bear, perfect for snuggling and comforting children of all ages.","ProductPrice": "$14.95"},
      {"ProductName": "Remote-Controlled Car","ProductDescription": "An exciting remote-controlled car with high-speed capabilities, providing hours of fun for kids and adults alike.","ProductPrice": "$29.99"},
      {"ProductName": "Art Supplies Kit","ProductDescription": "A complete art supplies kit including paints, brushes, and canvases for young artists to unleash their creativity.","ProductPrice": "$24.99"},
      {"ProductName": "Puzzle Game Set","ProductDescription": "A collection of challenging and educational puzzles that promote cognitive development and problem-solving skills.","ProductPrice": "$17.50"}
    ];
    // Function to display products
    function displayProducts(products){
      let productList = $('#product-list');
      productList.empty();
      products.forEach(product => {
        let card = `<div class=\"col s12 m6 l4\"><div class=\"card\"><div class=\"card-content\"><span class=\"card-title\">${product.ProductName}</span><p>${product.ProductDescription}</p><p><strong>${product.ProductPrice}</strong></p></div></div></div>`;
        productList.append(card);
      });
    }
    // Display all products initially
    displayProducts(allProducts);
    // Functionality for user search input
    $('#search').keyup(function(){
      let userInput = $(this).val().toLowerCase();
      let filteredProducts = allProducts.filter(product => product.ProductName.toLowerCase().includes(userInput));
      displayProducts(filteredProducts);
    });
  });