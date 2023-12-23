/* scripts.js */
$(document).ready(function(){
  const allProducts = [
    {
      "ProductName": "Building Blocks Set",
      "ProductDescription": "A creative set of colorful building blocks to inspire imaginative play and problem-solving skills.",
      "ProductPrice": "$19.99"
    },
    {
      "ProductName": "Stuffed Teddy Bear",
      "ProductDescription": "A soft and cuddly teddy bear, perfect for snuggling and comforting children of all ages.",
      "ProductPrice": "$14.95"
    },
    {
      "ProductName": "Remote-Controlled Car",
      "ProductDescription": "An exciting remote-controlled car with high-speed capabilities, providing hours of fun for kids and adults alike.",
      "ProductPrice": "$29.99"
    },
    {
      "ProductName": "Art Supplies Kit",
      "ProductDescription": "A complete art supplies kit including paints, brushes, and canvases for young artists to unleash their creativity.",
      "ProductPrice": "$24.99"
    },
    {
      "ProductName": "Puzzle Game Set",
      "ProductDescription": "A collection of challenging and educational puzzles that promote cognitive development and problem-solving skills.",
      "ProductPrice": "$17.50"
    }
  ];

  function displayProducts(products) {
    let html = '';
    products.forEach(product => {
      html += `
        <div class="col s12 m6 l4">
          <div class="card">
            <div class="card-content">
              <span class="card-title">${product.ProductName}</span>
              <p>${product.ProductDescription}</p>
              <p>${product.ProductPrice}</p>
            </div>
          </div>
        </div>`;
    });
    $('#products-list').html(html);
  }

  displayProducts(allProducts);
});